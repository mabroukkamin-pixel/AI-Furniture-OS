@echo off

cd /d %~dp0

call .venv\Scripts\activate

python -m brain.commander.command_router FULL

pause

