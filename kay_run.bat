@echo off
setlocal enabledelayedexpansion

:: Set Mister's home folder
set "MISTER_HOME=C:\Kaycris\MY_PROJECTS\Mister"

:: Run the command and capture output
set "cmd=%*"
set "tempfile=%TEMP%\kay_output.txt"

:: Run the command and save both stdout and stderr
%cmd% > "%tempfile%" 2>&1

:: Check if command failed (errorlevel != 0)
if %errorlevel% neq 0 (
    echo.
    echo [Mister] Crash detected! Saving error...
    
    :: Save the error to memory (using MISTER_HOME)
    type "%tempfile%" | py -c "import sys; import os; sys.path.insert(0, r'%MISTER_HOME%'); from tools.error_catcher import save_error; save_error(sys.stdin.read())"
    
    echo [Mister] Error saved. Type 'kay listen' to see details.
    echo.
)

:: Show the original output
type "%tempfile%"

:: Clean up
del "%tempfile%" 2>nul