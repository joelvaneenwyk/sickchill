@echo off
setlocal EnableExtensions
    call poetry run pip install --upgrade setuptools wheel
    call poetry run pip install --upgrade pytest-github-actions-annotate-failures
    call poetry install --no-interaction --with dev --with speedups
    call poetry run poe yarn
    call poetry run poe lint
    call poetry run poe yarn test
endlocal & goto:eof
