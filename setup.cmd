@echo off
setlocal EnableExtensions
    call sudo py -3 -m pip install --upgrade pip
    call py -3 -m pip install --user -r "%~dp0requirements.txt"

    call scoop install pipx
    call scoop update pipx
    call pipx install poetry

    set VIRTUAL_ENV_DISABLE_PROMPT=1
    call poetry shell

    call poetry run pip install --upgrade setuptools wheel
    call poetry run pip install --upgrade pytest-github-actions-annotate-failures
    call poetry install --no-interaction --with dev --with speedups
    call poetry run black .
    call poetry run poe yarn
    call poetry run poe lint
    call poetry run poe yarn test
endlocal & exit /b 0
