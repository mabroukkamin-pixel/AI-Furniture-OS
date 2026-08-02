@echo off

title AI FURNITURE OS V2 COMMAND CENTER


if "%1"=="FULL" (
python -m brain.commander.command_router FULL
goto END
)


if "%1"=="CHECK" (
python -m brain.commander.command_router CHECK
goto END
)


if "%1"=="AUTO" (
python -m brain.commander.command_router AUTO
goto END
)


if "%1"=="PRODUCTION" (
python -m brain.production.production_brain
goto END
)


if "%1"=="LOOP" (
python -m brain.autonomous.aifos_loop
goto END
)


if "%1"=="TEST" (
python -m brain.testing.release_test
goto END
)


if "%1"=="RELEASE" (
python -m brain.system.release_manager
goto END
)


echo.
echo =================================
echo AI FURNITURE OS V2 COMMAND CENTER
echo =================================
echo.
echo AIFOS FULL
echo AIFOS CHECK
echo AIFOS AUTO
echo AIFOS PRODUCTION
echo AIFOS LOOP
echo AIFOS TEST
echo AIFOS RELEASE
echo.


:END

