@echo off
REM Launch a new interactive PowerShell session directly from this batch script.
REM pw is alias to powershell

powershell.exe -NoExit -NoProfile -ExecutionPolicy Bypass %*
