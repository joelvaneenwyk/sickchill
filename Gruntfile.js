'use strict';

module.exports = function (grunt) {
  const CI = Boolean(process.env.CI);

  grunt.registerTask('default', [
    'clean',
    'bower',
    'bower_concat',
    'copy',
    'uglify',
    'cssmin',
  ]);

  grunt.registerTask('auto_update_trans', 'Update translations on master and push to master & develop', () => {
    if (!CI) {
      grunt.fatal('This task is only for CI!');
      return false;
    }

    grunt.log.writeln('Running grunt and updating translations...'.magenta);
    grunt.task.run([
      'exec:git:checkout:master',
      'default', // Run default task
      'exec:update_translations', // Update translations
      'exec:commit_changed_files:yes', // Determine what we need to commit if needed, stop if nothing to commit.
      'exec:git:reset --hard', // Reset unstaged changes (to allow for a rebase)
      'exec:git:checkout:develop', // Checkout develop
      'exec:git:rebase:master', // FF develop to the updated master
      'exec:git_push:origin:master develop', // Push master and develop
    ]);
  });

  /****************************************
    *  Admin only tasks                     *
    ****************************************/
  grunt.registerTask('publish', 'ADMIN: Create a new release tag and generate new CHANGES.md', [
    // 'exec:test', // Run tests
    'newrelease', // Pull and merge develop to master, create and push a new release
    'genchanges', // Update CHANGES.md
  ]);

  grunt.registerTask('reset_publishing', 'reset the repository back to clean master and develop from remote, and remove the local tag created to facilitate easier testing to the changes made here.', () => {
    if (CI) {
      grunt.fatal('This task not for CI!');
      return false;
    }

    grunt.log.writeln('Resetting the local repo back to remote heads for develop and master, and undoing any tags...'.red);
    grunt.task.run([
      'exec:check_return_branch', // Save the branch we are currently on, so we can return here
      'exec:git:checkout:master', // Checkout master
      'exec:git:reset --hard:origin/master', // Reset back to remote master
      'exec:git:checkout:develop', // Check out develop
      'exec:git:reset --hard:origin/develop', // Reset back to remote develop
      '_get_next_version:true', // To set the today string in grunt.config
      'exec:delete_today_tags', // Delete all local tags matching today's date
      'exec:git:fetch:origin --tags', // Pull tags back from remote
      'exec:check_return_branch:true', // Go back to the branch we were on

    ]);
  });
  grunt.registerTask('newrelease', 'Pull and merge develop to master, create and push a new release', [
    // Make sure we have the newest remote changes locally
    'exec:git:checkout:develop', // Switch to develop
    'exec:git:pull', // Pull develop
    'exec:git:checkout:master', // Switch to master
    'exec:git:pull', // Pull master

    // Set up old and new version strings
    '_get_last_version', // Get last tagged version
    '_get_next_version', // Get next version to set

    // Start merging and releasing
    'exec:git:merge:develop --strategy-option theirs', // Merge develop into master
    'exec:bump_version', // Update version in pyproject.toml
    'exec:commit_changed_files:yes', // Commit the new changed version
    'exec:git_list_changes', // List changes from since last tag
    'exec:git_tag_next_version', // Create new release tag
    'exec:git_push:origin:master:tags', // Push master + tags
    'exec:git:checkout:develop', // Go back to develop
    'exec:git:merge:master --strategy-option theirs', // Merge master back into develop
    'exec:git_push:origin:develop:tags', // Push develop + tags
  ]);

  grunt.registerTask('genchanges', 'Generate CHANGES.md file', () => {
    let file = grunt.option('file'); // --file=path/to/sickchill.github.io/sickchill-news/CHANGES.md
    if (!file) {
      file = process.env.SICKCHILL_CHANGES_FILE;
    }

    if (file && grunt.file.exists(file)) {
      grunt.config('changesmd_file', file.replaceAll('\\', '/')); // Use forward slashes only.
    } else {
      grunt.fatal('\tYou must provide a path to CHANGES.md to generate changes.\n'
                + '\t\tUse --file=path/to/sickchill.github.io/sickchill-news/CHANGES.md\n'
                + '\t\tor set the path in SICKCHILL_CHANGES_FILE (environment variable)');
    }

    grunt.task.run(['exec:git_list_tags', '_genchanges', 'exec:commit_changelog']);
  });

  /****************************************
    *  Task configurations                  *
    ****************************************/
  require('load-grunt-tasks')(grunt); // Loads all grunt tasks matching the ['grunt-*', '@*/grunt-*'] patterns
  grunt.initConfig({
    clean: {
      dist: './dist/',
      bower_components: './bower_components',
      fonts: './sickchill/gui/slick/css/fonts',
      options: {
        force: true,
      },
    },
    bower: {
      install: {
        options: {
          copy: false,
        },
      },
    },
    bower_concat: {
      all: {
        dest: {
          js: './dist/bower.js',
          css: './dist/bower.css',
        },
        exclude: [],
        dependencies: {},
        mainFiles: {
          tablesorter: [
            'dist/js/jquery.tablesorter.combined.min.js',
            'dist/js/parsers/parser-metric.min.js',
            'dist/js/widgets/widget-columnSelector.min.js',
            'dist/css/theme.blue.min.css',
          ],
          bootstrap: [
            'dist/css/bootstrap.min.css',
            'dist/js/bootstrap.min.js',
          ],
          'bootstrap-formhelpers': [
            'dist/js/bootstrap-formhelpers.min.js',
          ],
          isotope: [
            'dist/isotope.pkgd.min.js',
          ],
          outlayer: [
            'item.js',
            'outlayer.js',
          ],
          'open-sans-fontface': [
            '*.css',
            'fonts/**/*',
          ],
          'jqueryui-touch-punch': [
            'jquery.ui.touch-punch.min.js',
          ],
        },
        bowerOptions: {
          relative: false,
        },
      },
    },
    copy: {
      openSans: {
        files: [{
          expand: true,
          dot: true,
          cwd: 'bower_components/open-sans-fontface',
          src: [
            'fonts/**/*',
          ],
          dest: './sickchill/gui/slick/css/',
        }],
      },
      'fork-awesome': {
        files: [{
          expand: true,
          dot: true,
          cwd: 'bower_components/fork-awesome',
          src: [
            'fonts/**/*',
            'css/**/*.min.css',
            'css/**/*.css.map',
          ],
          dest: './sickchill/gui/slick/',
        }],
      },
      'font-awesome': {
        files: [{
          expand: true,
          dot: true,
          cwd: 'bower_components/font-awesome',
          src: [
            'fonts/**/*',
            'css/**/*.min.css',
            'css/**/*.css.map',
          ],
          dest: './sickchill/gui/slick/',
        }],
      },
      glyphicon: {
        files: [{
          expand: true,
          dot: true,
          cwd: 'bower_components/bootstrap/fonts',
          src: [
            '*.eot',
            '*.svg',
            '*.ttf',
            '*.woff',
            '*.woff2',
          ],
          dest: './sickchill/gui/slick/fonts/',
        }],
      },
    },
    uglify: {
      bower: {
        files: {
          './sickchill/gui/slick/js/vendor.min.js': ['./dist/bower.js'],
        },
      },
      core: {
        files: {
          './sickchill/gui/slick/js/core.min.js': ['./sickchill/gui/slick/js/core.js'],
        },
      },
    },
    cssmin: {
      options: {
        shorthandCompacting: false,
        roundingPrecision: -1,
      },
      bower: {
        files: {
          './sickchill/gui/slick/css/vendor.min.css': ['./dist/bower.css'],
        },
      },
      core: {
        files: {
          './sickchill/gui/slick/css/core.min.css': ['./dist/core.css'],
        },
      },
    },
    po2json: {
      messages: {
        options: {
          format: 'jed',
          singleFile: true,
        },
        files: [{
          expand: true,
          src: 'sickchill/locale/*/LC_MESSAGES/messages.po',
          dest: '',
          ext: '', // Workaround for relative files
        }],
      },
    },
    exec: {
      // Translations
      update_translations: {cmd: 'poe update_translations'},
      check_return_branch: {
        cmd(go_back) {
          let command = 'git branch --show-current';
          if (go_back) {
            command = 'git checkout ' + grunt.config('return_branch') + ' && ' + command;
          }

          return command;
        },
        stdout: false,
        callback(error, stdout) {
          stdout = stdout.trim();
          if (stdout.length === 0) {
            grunt.fatal('Could not find out what branch you were on!', 0);
          }

          grunt.config('return_branch', stdout);
        },
      },
      bump_version: {
        cmd() {
          return 'poetry version ' + grunt.config('next_version');
        },
        callback(error, stdout) {
          stdout = stdout.trim();
          if (stdout.length === 0) {
            grunt.fatal('No changes to commit.', 0);
          }

          if (!/Bumping version from \d{4}(?:\.\d{1,2}){2}(\.\d*)?/.test(stdout)) {
            grunt.fatal('Did the version update in pyproject.toml?');
          }
        },
      },

      // Delete tags from today
      delete_today_tags: {
        cmd() {
          return 'git tag -d $(git describe --match "' + grunt.config('today') + '*" --abbrev=0 --tags $(git rev-list --tags --max-count=1))';
        },
        stderr: false,
      },

      // Run tests
      test: {cmd: 'yarn run test || npm run test'},

      // Publish/Releases
      git: {
        cmd(cmd, branch) {
          branch = branch ? ' ' + branch : '';
          return 'git ' + cmd + branch;
        },
      },
      commit_changed_files: { // Choose what to commit.
        cmd(ci) {
          grunt.config('stop_no_changes', Boolean(ci));
          return 'git status -s -- pyproject.toml sickchill/locale/ sickchill/gui/';
        },
        stdout: false,
        callback(error, stdout) {
          stdout = stdout.trim();
          if (stdout.length === 0) {
            grunt.fatal('No changes to commit.', 0);
          }

          let commitMessage = [];
          const commitPaths = [];

          const isRelease = stdout.match(/pyproject.toml/gm);

          if (isRelease) {
            commitMessage.push('Release version ' + grunt.config('next_version'));
            commitPaths.push('pyproject.toml');
          }

          if (/sickchill\/gui\/.*(vendor|core)\.min\.(js|css)$/gm.test(stdout)) {
            if (!isRelease) {
              commitMessage.push('Grunt');
            }

            commitPaths.push('sickchill/gui/**/vendor.min.*', 'sickchill/gui/**/core.min.*');
          }

          if (/sickchill\/locale\/.*(pot|po|mo|json)$/gm.test(stdout)) {
            if (!isRelease) {
              commitMessage.push('Update translations');
            }

            commitPaths.push('sickchill/locale/');
          }

          if (commitMessage.length === 0 || commitPaths.length === 0) {
            if (grunt.config('stop_no_changes')) {
              grunt.fatal('Nothing to commit, aborting', 0);
            } else {
              grunt.log.ok('No extra changes to commit'.green);
            }
          } else {
            commitMessage = commitMessage.join(', ');
            if (process.env.GITHUB_RUN_ID && !isRelease) {
              commitMessage += ' (build ' + process.env.GITHUB_RUN_ID + ') [skip ci]';
            }

            grunt.config('commit_msg', commitMessage);
            grunt.config('commit_paths', commitPaths.join(' '));
            grunt.task.run('exec:commit_combined');
          }
        },
      },
      commit_combined: {
        cmd() {
          const message = grunt.config('commit_msg');
          const paths = grunt.config('commit_paths');
          if (!message || !paths) {
            grunt.fatal('Call exec:commit_changed_files instead!');
          }

          return 'git add -- ' + paths;
        },
        callback(error) {
          if (!error) {
            if (CI) { // Workaround for CI (with -m "text" the quotes are within the message)
              const messageFilePath = 'commit-msg.txt';
              grunt.file.write(messageFilePath, grunt.config('commit_msg'));
              grunt.task.run('exec:git:commit:-F ' + messageFilePath);
            } else {
              grunt.task.run('exec:git:commit:-m "' + grunt.config('commit_msg') + '"');
            }
          }
        },
      },
      git_list_changes: {
        cmd() {
          return 'git log --oneline --first-parent --pretty=format:%s ' + grunt.config('last_version') + '..HEAD';
        },
        stdout: false,
        callback(error, stdout) {
          const commits = stdout.trim()
            .replaceAll(/`/gm, '').replaceAll(/^\([\w\s,.\-+_/>]+\)\s/gm, '').replaceAll(/"/gm, '\\"'); // Removes ` and tag information
          if (commits) {
            grunt.config('commits', commits);
          } else {
            grunt.fatal('Getting new commit list failed!');
          }
        },
      },
      git_tag_next_version: {
        cmd(sign) {
          const next_version = grunt.config('next_version');
          grunt.log.ok(('Creating tag ' + next_version).green);
          sign = sign === 'true' ? '-s ' : '';
          return 'git tag ' + sign + next_version + ' -m "' + grunt.config('commits') + '"';
        },
        stdout: false,
      },
      git_push: {
        cmd(remote, branch, tags) {
          let pushCmd = 'git push ' + remote + ' ' + branch;
          if (tags) {
            pushCmd += ' --tags';
          }

          if (grunt.option('no-push')) {
            grunt.log.warn('Pushing with --dry-run ...'.magenta);
            pushCmd += ' --dry-run';
          }

          return pushCmd;
        },
        stderr: false,
        callback(error, stdout, stderr) {
          grunt.log.write(stderr.replace(process.env.GH_CRED, '[censored]'));
        },
      },
      git_list_tags: {
        cmd: 'git for-each-ref --sort=refname --format="%(refname:short)|||%(objectname)|||%(contents)\u00B6\u00B6\u00B6" refs/tags/20[0-9][0-9].[0-9][0-9].[0-9][0-9]*',
        stdout: false,
        callback(error, stdout) {
          if (!stdout) {
            grunt.fatal('Git command returned no data.');
          }

          if (error) {
            grunt.fatal('Git command failed to execute.');
          }

          const allTags = stdout
            .replaceAll(/-{5}BEGIN PGP SIGNATURE-{5}(.*\n)+?-{5}END PGP SIGNATURE-{5}\n/g, '')
            .split('\u00B6\u00B6\u00B6');
          const foundTags = [];
          for (const curTag of allTags) {
            if (curTag.length > 0) {
              const explode = curTag.split('|||');
              if (explode[0] && explode[1] && explode[2]) {
                foundTags.push({
                  tag: explode[0].trim(),
                  hash: explode[1].trim(),
                  message: explode[2].trim().split('\n'),
                  previous: (foundTags.length > 0 ? foundTags.at(-1).tag : null),
                });
              }
            }
          }

          if (foundTags.length > 0) {
            grunt.config('all_tags', foundTags.reverse()); // LIFO
          } else {
            grunt.fatal('Could not get existing tags information');
          }
        },
      },
      commit_changelog: {
        cmd() {
          const file = grunt.config('changesmd_file');
          if (!file) {
            grunt.fatal('Missing file path.');
          }

          const path = file.slice(0, -25); // Slices 'sickchill-news/CHANGES.md' (len=25)
          if (!path) {
            grunt.fatal('path = "' + path + '"');
          }

          let pushCmd = 'git push origin master';
          if (grunt.option('no-push')) {
            grunt.log.warn('Pushing with --dry-run ...'.magenta);
            pushCmd += ' --dry-run';
          }

          return ['cd ' + path,
            'git commit -asm "Update changelog"',
            'git fetch origin',
            'git rebase',
            pushCmd].join(' && ');
        },
        stdout: true,
      },
    },
  });

  /****************************************
    *  Internal tasks                       *
    *****************************************/
  grunt.registerTask('_get_last_version', '(internal) do not run', () => {
    const toml = require('toml');

    const file = './pyproject.toml';
    if (!grunt.file.exists(file)) {
      grunt.fatal('Could not find pyproject.toml, cannot proceed');
    }

    const version = toml.parse(grunt.file.read(file)).tool.poetry.version;
    if (version === null) {
      grunt.fatal('Error processing pyproject.toml, cannot proceed');
    }

    grunt.config('last_version', version);
  });

  grunt.registerTask('_get_next_version', '(internal) do not run', skip_post => {
    const date_object = new Date();
    const year = date_object.getFullYear();
    const day = date_object.getDate();
    const month = date_object.getMonth() + 1;
    const hours = date_object.getUTCHours();
    const minutes = date_object.getUTCMinutes();
    const seconds = date_object.getUTCSeconds();

    let next_version = year.toString() + '.' + month.toString().padStart(2 - month.length, '0') + '.' + day.toString().padStart(2 - day.length, '0');
    grunt.config('today', next_version); // Needed for resetting failed publishing.

    if (skip_post) {
      return;
    }

    const last_version = grunt.config('last_version');
    if (last_version === undefined || last_version.length === 0) {
      grunt.fatal('Must call _get_last_version first!');
    }

    if (next_version === last_version) {
      grunt.fatal('Let\'s only release once a day, or semver is broken. We can fix this when we do away with grunt');
      next_version += '.' + hours + minutes + seconds;
    }

    grunt.config('next_version', next_version);
  });

  grunt.registerTask('_genchanges', '(internal) do not run', () => {
    // Actual generate changes
    const allTags = grunt.config('all_tags');
    if (!allTags) {
      grunt.fatal('No tags information was received.');
    }

    const file = grunt.config('changesmd_file'); // --file=path/to/sickchill.github.io/sickchill-news/CHANGES.md
    if (!file) {
      grunt.fatal('Missing file path.');
    }

    let contents = '';
    for (const tag of allTags) {
      contents += '### ' + tag.tag + '\n';
      contents += '\n';
      if (tag.previous) {
        contents += '[full changelog](https://github.com/joelvaneenwyk/SickChill/compare/'
                    + tag.previous + '...' + tag.tag + ')\n';
      }

      contents += '\n';
      for (const row of tag.message) {
        contents += row
        // Link issue n return 'git tag ' + grunt.config('next_version') + ' -sm "' + grunt.config('commits') + '"';umbers, style links of issues and pull requests
          .replaceAll(/([\w\-.]+\/[\w\-.]+)?#(\d+)|https?:\/\/github.com\/([\w\-.]+\/[\w\-.]+)\/(issues|pull)\/(\d+)/gm,
            (all, repoL, numberL, repoR, typeR, numberR) => {
              if (numberL) { // RepoL, numL = user/repo#1234 style
                return '[' + (repoL ? repoL : '') + '#' + numberL + '](https://github.com/'
                                    + (repoL ? repoL : 'SickChill/SickChill') + '/issues/' + numberL + ')';
              }

              if (numberR) { // RepoR, type, numR = https://github/user/repo/issues/1234 style
                return '[#' + numberR + ']' + '(https://github.com/'
                                    + repoR + '/' + typeR + '/' + numberR + ')';
              }
            })
        // Shorten and link commit hashes
          .replaceAll(/([a-f\d]{40}(?![a-f\d]))/g, sha1 => '[' + sha1.slice(0, 7) + '](https://github.com/joelvaneenwyk/SickChill/commit/' + sha1 + ')')
        // Remove tag information
          .replaceAll(/^\([\w\s,.\-+/>]+\)\s/gm, '')
        // Remove commit hashes from start
          .replaceAll(/^[a-f\d]{7} /gm, '')
        // Style messages that contain lists
          .replaceAll(/( {3,}\*)(?!\*)/g, '\n  -')
        // Escapes markdown __ tags
          .replaceAll(/__/gm, '\\_\\_')
        // Add * to the first line only
          .replace(/^(\w)/, '* $1');

        contents += '\n';
      }

      contents += '\n';
    }

    if (contents) {
      grunt.file.write(file, contents);
      return true;
    }

    grunt.fatal('Received no contents to write to file, aborting');
  });
};
