::
:: Start Pylp via the terminal.
::
:: Copyright (C) 2017, Guillaume Gonnet
:: This file is under the MIT License.
@echo off
setlocal

:: Test if Python 3 is called "python3" or just "python"
where python3 >nul 2>nul
if %ERRORLEVEL% EQU 0 (
     set PYTHON=python3
) else (
     set PYTHON=python
)

:: Test if python is installed and in the PATH
where %PYTHON% >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not in your PATH.
    exit /b
)

:: Checks the version of Python
for /f "tokens=*" %%i in ('%PYTHON% -c "import sys;print(sys.version_info[0])"') do set PYTHON_VER=%%i
if "%PYTHON_VER:~0,1%" NEQ "3" (
    echo You must have Python 3 to execute Pylp.
    exit /b
)

:: Start Pylp
%PYTHON% "%~dp0pylp\cli\cli.py" %*
