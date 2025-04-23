echo "this script was converted to batch from the bash script setup.sh. It is untested. Here be dragons"

@echo off
setlocal enabledelayedexpansion

REM Default flags
set "compile_docs=true"
set "install=true"

REM Parse arguments
:parse_args
if "%~1"=="" goto after_args

if "%~1"=="--create-venv" (
    python -m venv .venv
    echo Virtual environment created.
    echo You must activate it using:
    echo     call .venv\Scripts\activate
)

if "%~1"=="--no-docs" (
    set "compile_docs=false"
)

if "%~1"=="--no-install" (
    set "install=false"
)

shift
goto parse_args

:after_args

REM Check for python
where python >nul 2>&1
if errorlevel 1 (
    echo Error: python is not installed.
    echo Install it: https://www.python.org/downloads/windows/
    exit /b 1
)

REM Check for pip
where pip >nul 2>&1
if errorlevel 1 (
    echo Error: pip is not installed.
    echo Install it: https://www.python.org/downloads/windows/
    exit /b 1
)

REM Check if inside a venv
if not defined VIRTUAL_ENV (
    if not exist ".venv\Scripts\activate.bat" (
        echo Error: No virtual environment found.
        echo Use --create-venv to create one.
        exit /b 1
    )
    echo Warning: This script should be run from inside the virtual environment.
    echo Run: call .venv\Scripts\activate
    exit /b 1
)

REM Install dependencies
if "%install%"=="true" (
    pip install -r requirements.txt
)

REM Compile documentation
if "%compile_docs%"=="true" (
    if exist docs (
        cd docs
        call make clean
        call make html
        start "" "..\_build\html\index.html"
        cd ..
    ) else (
        echo docs directory not found
    )
)

endlocal