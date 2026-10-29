@echo off
title CS2 SKIN LOADER
cd /d "%~dp0"

echo ========================================================
echo        CS2 SKIN AND INVENTORY LOADER
echo ========================================================
echo.

where python >nul 2>nul
if %errorlevel% equ 0 (
    set "PY_EXE=python"
) else (
    where py >nul 2>nul
    if %errorlevel% equ 0 (
        set "PY_EXE=py"
    ) else (
        if exist "%LOCALAPPDATA%\Programs\Python\Python314\python.exe" (
            set "PY_EXE=%LOCALAPPDATA%\Programs\Python\Python314\python.exe"
        ) else (
            set "PY_EXE=python"
        )
    )
)

echo [OK] Lancement du loader...
echo.

"%PY_EXE%" main.py

if errorlevel 1 (
    echo.
    echo ========================================================
    echo [ERREUR] L'application s'est fermee avec un probleme.
    echo ========================================================
    pause
)
