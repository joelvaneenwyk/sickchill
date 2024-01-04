@echo off
goto:$Main

goto:$Command
:Command
    goto:$CommandVar
    :CommandVar
        setlocal EnableDelayedExpansion
        set "_command=!%~1!"
        set "_command=!_command:      = !"
        set "_command=!_command:    = !"
        set "_command=!_command:   = !"
        set "_command=!_command:  = !"
        set _error_value=0
        if "%MYCOSHIRO_CRITICAL_ERROR%"=="" goto:$RunCommand
        if "%MYCOSHIRO_CRITICAL_ERROR%"=="0" goto:$RunCommand

        :: Hit critical error so skip the command
        echo [ERROR] Critical error detected. Skipped command: !_command!
        set _error_value=%MYCOSHIRO_CRITICAL_ERROR%
        goto:$CommandDone

        :$RunCommand
        echo ##[cmd] !_command!
        call !_command!
        set _error_value=%ERRORLEVEL%

        :$CommandDone
        endlocal & (
            exit /b %_error_value%
        )
    :$CommandVar

    setlocal EnableDelayedExpansion
        set "_command=%*"
        call :CommandVar "_command"
    endlocal & exit /b
:$Command

:$Main
setlocal EnableExtensions
    call :Command npm install -g npm-check-updates
    if errorlevel 1 goto:$MainError

    call :Command sudo corepack enable
    if errorlevel 1 goto:$MainError

    call :Command corepack yarn install
    if errorlevel 1 goto:$MainError

    call :Command sudo py -3 -m pip install --upgrade pip
    if errorlevel 1 goto:$MainError
    call :Command py -3 -m pip install --user -r "%~dp0requirements.txt"
    if errorlevel 1 goto:$MainError

    call :Command scoop install pipx
    if errorlevel 1 goto:$MainError
    call :Command scoop update pipx
    if errorlevel 1 goto:$MainError
    call :Command pipx install poetry
    if errorlevel 1 goto:$MainError

    set VIRTUAL_ENV_DISABLE_PROMPT=1
    call :Command poetry shell

    call :Command poetry run pip install --upgrade pip setuptools wheel pytest-github-actions-annotate-failures
    if errorlevel 1 goto:$MainError

    call :Command poetry install --no-interaction --with dev --with speedups
    if errorlevel 1 goto:$MainError

    call :Command poetry run black .
    if errorlevel 1 goto:$MainError

    call :Command poetry run poe yarn
    if errorlevel 1 goto:$MainError

    call :Command poetry run poe lint
    if errorlevel 1 goto:$MainError

    call :Command poetry run poe yarn test
    if errorlevel 1 goto:$MainError
    goto:$MainDone

    :$MainError
        echo [Error] Error during setup. Error level: '%ERRORLEVEL%'
        goto:$MainDone

    :$MainDone
endlocal & exit /b 0
