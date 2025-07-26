@echo off
REM This Windows script is used to launch an MSYS2/UCRT64 shell or execute a command in it.
REM Install to C:\MyScripts\ucrt.bat (use mklinks or just copy it to C:\MyScripts\)
REM echo "%*"

REM Set before IF
SET BASH_COMMAND="%*"

REM Path to your msys2_shell.cmd
SET "MSYS2_SHELL_PATH=C:\tools\msys64\msys2_shell.cmd"
SET "MSYS2_SHELL_OPTS=-defterm -no-start -ucrt64 -here"

REM Check if any arguments (parameters) were passed to the Batch script
IF "%*"=="" (
    REM No arguments - launch an interactive MSYS2/UCRT64 shell
    echo Launching interactive Bash UCRT64 shell...
    %MSYS2_SHELL_PATH% %MSYS2_SHELL_OPTS%
) ELSE (
    REM Arguments provided - concatenate them and execute as a command in Bash
    echo Executing Bash UCRT64 command: %BASH_COMMAND%
    %MSYS2_SHELL_PATH% %MSYS2_SHELL_OPTS% -c %BASH_COMMAND%
)
