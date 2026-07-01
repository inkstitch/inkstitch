@echo off
set SCRIPT_DIR=%~dp0
uv --project "%SCRIPT_DIR%" run python "%SCRIPT_DIR%inkstitch.py" %*
