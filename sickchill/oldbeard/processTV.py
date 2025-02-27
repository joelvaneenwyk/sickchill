import logging
import os
import shutil
import stat
import traceback
from pathlib import Path
from typing import TYPE_CHECKING

import validators
from rarfile import BadRarFile, Error, NeedFirstVolume, PasswordRequired, RarCRCError, RarExecError, RarFile, RarOpenError, RarWrongPassword

from sickchill import logger, settings
from sickchill.helper.common import is_media_file, is_rar_file, is_sync_file, is_torrent_or_nzb_file, remove_extension
from sickchill.helper.exceptions import EpisodePostProcessingFailedException, FailedPostProcessingFailedException

from . import common, db, failedProcessor, helpers, postProcessor

if TYPE_CHECKING:
    from sickchill.oldbeard.name_parser.parser import ParseResult


class ProcessResult(object):
    def __init__(self):
        self.result = True
        self.output = ""
        self.missed_files = []
        self.aggresult = True


def delete_folder(folder, check_empty=True):
    """
    Removes a folder from the filesystem

    param folder: Path to folder to remove
    param check_empty: Boolean, check if the folder is empty before removing it, defaults to True
    return: True on success, False on failure
    """

    # check if it's a folder
    if not os.path.isdir(folder):
        return False

    # check if it isn't TV_DOWNLOAD_DIR
    if settings.TV_DOWNLOAD_DIR and helpers.real_path(folder) == helpers.real_path(settings.TV_DOWNLOAD_DIR):
        return False

    # check if it's empty folder when wanted to be checked
    if check_empty:
        check_files = os.listdir(folder)
        if check_files:
            logger.info(f"Not deleting folder {folder} found the following files: {check_files}")
            return False

        try:
            logger.info(f"Deleting folder (if it's empty): {folder}")
            os.rmdir(folder)
        except (OSError, IOError) as error:
            logger.warning(f"Warning: unable to delete folder: {folder}: {error}")
            return False
    else:
        try:
            logger.info("Deleting folder: " + folder)
            shutil.rmtree(folder)
        except (OSError, IOError) as error:
            logger.warning(f"Warning: unable to delete folder: {folder}: {error}")
            return False

    return True


def delete_files(process_path, unwanted_files, result, force=False):
    """
    Remove files from filesystem

    param process_path: path to process
    param unwanted_files: files we do not want
    param result: Processor results
    param force: Boolean, force deletion, defaults to false
    """
    if not result.result and force:
        result.output += log_helper("Forcing deletion of files, even though last result was not success", logger.DEBUG)
    elif not result.result:
        return

    # Delete all file not needed
    for cur_file in unwanted_files:
        cur_file_path = os.path.join(process_path, cur_file)
        if not os.path.isfile(cur_file_path):
            continue  # Prevent error when a notwantedfiles is an associated files

        result.output += log_helper(f"Deleting file: {cur_file}", logger.DEBUG)

        # check first the read-only attribute
        file_attribute = os.stat(cur_file_path)[0]
        if not file_attribute & stat.S_IWRITE:
            # File is read-only, so make it writeable
            result.output += log_helper(f"Changing ReadOnly Flag for file: {cur_file}", logger.DEBUG)
            try:
                os.chmod(cur_file_path, stat.S_IWRITE)
            except OSError as error:
                result.output += log_helper(f"Cannot change permissions of {cur_file_path}: {error}", logger.DEBUG)
        try:
            os.remove(cur_file_path)
        except OSError as error:
            result.output += log_helper(f"Unable to delete file {cur_file}: {error}", logger.DEBUG)


def log_helper(message, level=logging.INFO):
    logger.log(level, message)
    return message + "\n"


def process_dir(process_path, release_name=None, process_method=None, force=False, is_priority=None, delete_on=False, failed=False, mode="auto"):
    """
    Scans through the files in process_path and processes whatever media files it finds

    param process_path: The folder name to look in
    param release_name: The NZB/Torrent name which resulted in this folder being downloaded
    param process_method: processing method, copy/move/symlink/link
    param force: True to process previously processed files
    param is_priority: whether to replace the file even if it exists at higher quality
    param delete_on: delete files and folders after they are processed (always happens with move and auto combination)
    param failed: Boolean for whether the download failed
    param mode: Type of postprocessing auto or manual
    """
    result = ProcessResult()
    try:
        # if they passed us a real dir then assume it's the one we want
        if os.path.isdir(process_path):
            process_path = os.path.realpath(process_path)
            result.output += log_helper(f"Processing in folder {process_path}", logger.DEBUG)

        # if the client and SickChill are not on the same machine translate the directory into a network directory
        elif all(
            [settings.TV_DOWNLOAD_DIR, os.path.isdir(settings.TV_DOWNLOAD_DIR), os.path.normpath(process_path) == os.path.normpath(settings.TV_DOWNLOAD_DIR)]
        ):
            process_path = os.path.join(settings.TV_DOWNLOAD_DIR, os.path.abspath(process_path).split(os.path.sep)[-1])
            result.output += log_helper(f"Trying to use folder: {process_path} ", logger.DEBUG)

        # if we didn't find a real dir then quit
        if not os.path.isdir(process_path):
            result.output += log_helper(
                "Unable to figure out what folder to process. "
                "If your downloader and SickChill aren't on the same PC "
                "make sure you fill out your TV download dir in the config.",
                logger.DEBUG,
            )
            return result.output

        process_method = process_method or settings.PROCESS_METHOD

        directories_from_rars = set()

        # If we have a release name (probably from nzbToMedia), and it is a rar/video, only process that file
        if release_name and validators.url(release_name) is True:
            result.output += log_helper(_("Processing {release_name}").format(release_name=release_name))
            generator_to_use = [("", [], [release_name])]
        elif release_name and (is_media_file(release_name) or is_rar_file(release_name)):
            result.output += log_helper(_("Processing {release_name}").format(release_name=release_name))
            generator_to_use = [(process_path, [], [release_name])]
        else:
            result.output += log_helper(_("Processing {process_path}").format(process_path=process_path))
            generator_to_use = os.walk(process_path, followlinks=settings.PROCESSOR_FOLLOW_SYMLINKS)

        for current_directory, directory_names, filenames in generator_to_use:
            result.result = True

            if current_directory:
                filenames = [f for f in filenames if not is_torrent_or_nzb_file(f)]
                rar_files = [x for x in filenames if is_rar_file(os.path.join(current_directory, x))]
                if rar_files:
                    extracted_directories = unrar(current_directory, rar_files, force, result)
                    if extracted_directories:
                        for extracted_directory in extracted_directories:
                            if extracted_directory.split(current_directory)[-1] not in directory_names:
                                result.output += log_helper(
                                    _("Adding extracted directory to the list of directories to process: {extracted_directory}").format(
                                        extracted_directory=extracted_directory
                                    ),
                                    logger.DEBUG,
                                )
                                directories_from_rars.add(extracted_directory)

            if not validate_dir(current_directory, release_name, failed, result):
                continue

            video_files = list(filter(is_media_file, filenames))
            if video_files:
                process_media(current_directory, video_files, release_name, process_method, force, is_priority, result)
            else:
                result.result = False

            # Delete all file not needed and avoid deleting files if Manual PostProcessing
            if not (process_method == "move" and result.result) or (mode == "manual" and not delete_on):
                continue

            # noinspection PyTypeChecker
            unwanted_files = [x for x in filenames if x in video_files + rar_files]
            if unwanted_files:
                result.output += log_helper(_("Found unwanted files: {unwanted_files}").format(unwanted_files=unwanted_files), logger.DEBUG)

            delete_folder(os.path.join(current_directory, "@eaDir"), False)
            delete_files(current_directory, unwanted_files, result)
            if delete_folder(current_directory, check_empty=not delete_on):
                result.output += log_helper(_("Deleted folder: {current_directory}").format(current_directory=current_directory), logger.DEBUG)

        # For processing extracted rars, only allow methods 'move' and 'copy'.
        # On different methods fall back to 'move'.
        method_fallback = ("move", process_method)[process_method in ("move", "copy")]

        for directory_from_rar in directories_from_rars:
            process_dir(
                process_path=directory_from_rar,
                release_name=os.path.basename(directory_from_rar),
                process_method=method_fallback,
                force=force,
                is_priority=is_priority,
                delete_on=settings.DELRARCONTENTS or delete_on or method_fallback == "move",
                failed=failed,
                mode=mode,
            )

            # Delete rar file only if the extracted dir was successfully processed
            if mode == "auto" and method_fallback == "move" or mode == "manual" and delete_on:
                this_rar = [rar_file for rar_file in rar_files if Path(directory_from_rar).name == Path(rar_file).stem]
                delete_files(current_directory, this_rar, result)  # Deletes only if result.result == True

            delete_folder(directory_from_rar, settings.DELRARCONTENTS)

        result.output += log_helper((_("Processing Failed"), _("Successfully processed"))[result.aggresult], (logger.WARNING, logger.INFO)[result.aggresult])
        if result.missed_files:
            result.output += log_helper(_("Some items were not processed."))
            for missed_file in result.missed_files:
                result.output += log_helper(missed_file)

        return result.output
    except Exception:
        logger.debug(traceback.format_exc())
        return result.output


def validate_dir(process_path, release_name, failed, result):
    """
    Check if directory is valid for processing

    param process_path: Directory to check
    param release_name: Original NZB/Torrent name
    param failed: Previously failed objects
    param result: Previous results
    returns True if dir is valid for processing, False if not
    """

    result.output += log_helper("Processing folder " + process_path, logger.DEBUG)
    upper_name = os.path.basename(process_path).upper()
    if upper_name.startswith("_FAILED_") or upper_name.endswith("_FAILED_") or (os.sep + "_FAILED_") in upper_name or ("_FAILED_" + os.sep) in upper_name:
        result.output += log_helper(_("The directory name indicates it failed to extract."), logger.DEBUG)
        failed = True
    elif (
        upper_name.startswith("_UNDERSIZED_")
        or upper_name.endswith("_UNDERSIZED_")
        or (os.sep + "_UNDERSIZED_") in upper_name
        or ("_UNDERSIZED_" + os.sep) in upper_name
    ):
        result.output += log_helper(_("The directory name indicates that it was previously rejected for being undersized."), logger.DEBUG)
        failed = True
    elif upper_name.startswith("_UNPACK") or upper_name.endswith("_UNPACK") or (os.sep + "_UNPACK") in upper_name or ("_UNPACK" + os.sep) in upper_name:
        result.output += log_helper(_("The directory name indicates that this release is in the process of being unpacked."), logger.DEBUG)
        result.missed_files.append(f"{process_path} : Being unpacked")
        return False

    if failed:
        process_failed(process_path, release_name, result)
        result.missed_files.append(f"{process_path} : Failed download")
        return False

    if settings.TV_DOWNLOAD_DIR and helpers.real_path(process_path) != helpers.real_path(settings.TV_DOWNLOAD_DIR) and helpers.is_hidden_folder(process_path):
        result.output += log_helper(f"Ignoring hidden folder: {process_path}", logger.DEBUG)
        if not process_path.endswith("@eaDir"):
            result.missed_files.append(f"{process_path} : Hidden folder")
        return False

    # make sure the dir isn't inside a show dir
    main_db_con = db.DBConnection()
    sql_results = main_db_con.select("SELECT location FROM tv_shows")

    for sqlShow in sql_results:
        if (
            process_path.lower().startswith(os.path.realpath(sqlShow["location"]).lower() + os.sep)
            or process_path.lower() == os.path.realpath(sqlShow["location"]).lower()
        ):
            result.output += log_helper("Cannot process an episode that's already been moved to its show dir, skipping " + process_path, logger.WARNING)
            return False

    for current_directory, directory_names, filenames in os.walk(process_path, topdown=False, followlinks=settings.PROCESSOR_FOLLOW_SYMLINKS):
        sync_files = list(filter(is_sync_file, filenames))
        if sync_files and settings.POSTPONE_IF_SYNC_FILES:
            result.output += log_helper(f"Found temporary sync files: {sync_files} in path: {os.path.join(process_path, sync_files[0])}")
            result.output += log_helper(f"Skipping post processing for folder: {process_path}")
            result.missed_files.append(f"{os.path.join(process_path, sync_files[0])} : Sync files found")
            continue

        found_files = list(filter(is_media_file, filenames))
        if settings.UNPACK == settings.UNPACK_PROCESS_CONTENTS:
            found_files += list(filter(is_rar_file, filenames))

        for found_file in found_files:
            if current_directory != settings.TV_DOWNLOAD_DIR and found_files:
                # pass 'current directory/filename' as one string to NameParser
                found_file = f"{os.path.basename(current_directory)}/{found_file}"

            if postProcessor.guessit_findit(found_file):
                return True

    result.output += log_helper(f"{process_path} : No processable items found in folder", logger.DEBUG)
    return False


def unrar(path, rar_files, force, result):
    """
    Extracts RAR files

    param path: Path to look for files in
    param rar_files: Names of RAR files
    param force: process currently processing items
    param result: Previous results
    returns List of unpacked file names
    """

    unpacked_dirs = []

    if settings.UNPACK == settings.UNPACK_PROCESS_CONTENTS and rar_files:
        result.output += log_helper(f"Packed Releases detected: {rar_files}", logger.DEBUG)
        for archive in rar_files:
            failure = None
            rar_handle = None
            try:
                archive_path = os.path.join(path, archive)
                if already_processed(path, archive, force, result):
                    result.output += log_helper(f"Archive file already post-processed, extraction skipped: {archive_path}", logger.DEBUG)
                    continue

                if not is_rar_file(archive_path):
                    continue

                result.output += log_helper(f"Checking if archive is valid and contains a video: {archive_path}", logger.DEBUG)
                rar_handle = RarFile(archive_path)
                if rar_handle.needs_password():
                    # TODO: Add support in settings for a list of passwords to try here with rar_handle.set_password(x)
                    result.output += log_helper(f"Archive needs a password, skipping: {archive_path}")
                    continue

                rar_handle.testrar()

                # If there are no video files in the rar, don't extract it
                rar_media_files = list(filter(is_media_file, rar_handle.namelist()))
                if not rar_media_files:
                    continue

                rar_release_name = Path(archive).stem

                # Choose the directory we'll unpack to:
                if settings.UNPACK_DIR and os.path.isdir(settings.UNPACK_DIR):  # verify that the unpacked dir exists
                    unpack_base_dir = settings.UNPACK_DIR
                else:
                    unpack_base_dir = path
                    if settings.UNPACK_DIR:  # Let user know if we can't unpack there
                        result.output += log_helper(f"Unpack directory cannot be verified. Using {path}", logger.DEBUG)

                # Fix up the list for checking if already processed
                rar_media_files = [os.path.join(unpack_base_dir, rar_release_name, rar_media_file) for rar_media_file in rar_media_files]

                skip_rar = False
                for rar_media_file in rar_media_files:
                    check_path, check_file = os.path.split(rar_media_file)
                    if already_processed(check_path, check_file, force, result):
                        result.output += log_helper(f"Archive file already post-processed, extraction skipped: {rar_media_file}", logger.DEBUG)
                        skip_rar = True
                        break

                if skip_rar:
                    continue

                rar_extract_path = os.path.join(unpack_base_dir, rar_release_name)
                result.output += log_helper(f"Unpacking archive: {archive}", logger.DEBUG)
                rar_handle.extractall(path=rar_extract_path)
                unpacked_dirs.append(rar_extract_path)

            except RarCRCError:
                failure = ("Archive Broken", "Unpacking failed because of a CRC error")
            except RarWrongPassword:
                failure = ("Incorrect RAR Password", "Unpacking failed because of an Incorrect Rar Password")
            except PasswordRequired:
                failure = ("Rar is password protected", "Unpacking failed because it needs a password")
            except RarOpenError:
                failure = (
                    "Rar Open Error, check the parent folder and destination file permissions.",
                    "Unpacking failed with a File Open Error (file permissions?)",
                )
            except RarExecError:
                failure = ("Invalid Rar Archive Usage", "Unpacking Failed with Invalid Rar Archive Usage. Is unrar installed and on the system PATH?")
            except BadRarFile:
                failure = ("Invalid Rar Archive", "Unpacking Failed with an Invalid Rar Archive Error")
            except NeedFirstVolume:
                continue
            except (Exception, Error) as error:
                failure = (error, "Unpacking failed")
            finally:
                if rar_handle:
                    del rar_handle

            if failure:
                result.output += log_helper(f"Failed to extract the archive {archive}: {failure[0]}", logger.WARNING)
                result.missed_files.append(f"{archive} : Unpacking failed: {failure[1]}")
                result.result = False
                continue

    return unpacked_dirs


def already_processed(process_path, video_file, force, result):
    """
    Check if we already post processed a file

    param process_path: Directory a file resides in
    param video_file: File name
    param force: Force checking when already checking (currently unused)
    param result: True if file is already postprocessed, False if not
    :return:
    """
    if force:
        return False

    # Avoid processing the same dir again if we use a process method <> move
    main_db_con = db.DBConnection()
    sql_result = main_db_con.select("SELECT release_name FROM tv_episodes WHERE release_name IN (?, ?) LIMIT 1", [process_path, remove_extension(video_file)])
    if sql_result:
        # result.output += log_helper("You're trying to post process a dir that's already been processed, skipping", logger.DEBUG)
        return True

    # Needed if we have downloaded the same episode @ different quality
    # But we need to make sure we check the history of the episode we're going to PP, and not others
    # if it fails to find any info (because we're doing an unparsable folder (like the TV root dir) it will throw an exception, which we want to ignore
    parse_result: "ParseResult" = postProcessor.guessit_findit(process_path)

    search_sql = "SELECT tv_episodes.indexerid, history.resource FROM tv_episodes INNER JOIN history ON history.showid=tv_episodes.showid"  # This part is always the same
    search_sql += " WHERE history.season=tv_episodes.season AND history.episode=tv_episodes.episode"

    # If we find a showid, a season number, and one or more episode numbers than we need to use those in the query
    if parse_result:
        if parse_result.show.indexerid:
            search_sql += f" AND tv_episodes.showid={parse_result.show.indexerid}"
        if parse_result.season_number is not None and parse_result.episode_numbers:
            search_sql += f" AND tv_episodes.season={parse_result.season_number} AND tv_episodes.episode={parse_result.episode_numbers[0]}"
        elif parse_result.ab_episode_numbers:
            search_sql += f" AND tv_episodes.showid={parse_result.show.indexerid} AND tv_episodes.absolute_number={parse_result.ab_episode_numbers[0]}"

    search_sql += " AND tv_episodes.status IN (" + ",".join([str(x) for x in common.Quality.DOWNLOADED + common.Quality.ARCHIVED]) + ")"
    search_sql += " AND history.resource LIKE ? LIMIT 1"
    sql_result = main_db_con.select(search_sql, ["%" + video_file])
    if sql_result:
        result.output += log_helper("You're trying to post process a video that's already been processed, skipping", logger.DEBUG)
        return True

    return False


def process_media(process_path, video_files, release_name, process_method, force, is_priority, result):
    """
    Postprocess mediafiles

    param process_path: Path to process in
    param video_files: Filenames to look for and postprocess
    param release_name: Name of NZB/Torrent file related
    param process_method: auto/manual
    param force: Postprocess currently postprocessing file
    param is_priority: Boolean, is this a priority download
    param result: Previous results
    """

    processor = None
    for cur_video_file in video_files:
        cur_video_file_path = os.path.join(process_path, cur_video_file)

        if already_processed(process_path, cur_video_file, force, result):
            result.output += log_helper(f"Skipping already processed file: {cur_video_file}", logger.DEBUG)
            continue

        try:
            processor = postProcessor.PostProcessor(cur_video_file_path, release_name, process_method, is_priority)
            result.result = processor.process()
            process_fail_message = ""
        except EpisodePostProcessingFailedException as error:
            result.result = False
            process_fail_message = error

        if processor:
            result.output += processor.log

        if result.result:
            result.output += log_helper(f"Processing succeeded for {cur_video_file_path}")
        else:
            result.output += log_helper(f"Processing failed for {cur_video_file_path}: {process_fail_message}", logger.WARNING)
            result.missed_files.append(f"{cur_video_file_path} : Processing failed: {process_fail_message}")
            result.aggresult = False


def process_failed(process_path, release_name, result):
    """Process a download that did not complete correctly"""

    if not settings.USE_FAILED_DOWNLOADS:
        return

    processor = None

    try:
        processor = failedProcessor.FailedProcessor(process_path, release_name)
        result.result = processor.process()
        process_fail_message = ""
    except FailedPostProcessingFailedException as error:
        result.result = False
        process_fail_message = error

    if processor:
        result.output += processor.log

    if settings.DELETE_FAILED and result.result:
        if delete_folder(process_path, check_empty=False):
            result.output += log_helper(f"Deleted folder: {process_path}", logger.DEBUG)

    if result.result:
        result.output += log_helper(f"Failed Download Processing succeeded: ({release_name}, {process_path})")
    else:
        result.output += log_helper(f"Failed Download Processing failed: ({release_name}, {process_path}): {process_fail_message}", logger.WARNING)
