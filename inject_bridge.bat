@echo off
setlocal enabledelayedexpansion
title ARCEUS // CS2 BRIDGE INJECTOR

cd /d "%~dp0"

echo ===================================================
echo [ARCEUS] Injection de mesa_bridge.dll dans cs2.exe
echo ===================================================

if not exist "native\mesa_injector.exe" (
    echo [ERREUR] native\mesa_injector.exe est introuvable.
    pause
    exit /b 1
)

if not exist "native\mesa_bridge.dll" (
    echo [ERREUR] native\mesa_bridge.dll est introuvable.
    pause
    exit /b 1
)

tasklist /FI "IMAGENAME eq cs2.exe" 2>NUL | find /I /N "cs2.exe" >NUL
if %ERRORLEVEL% neq 0 (
    echo [ATTENTION] cs2.exe n'est pas detecte en cours d'execution.
    echo Veuillez d'abord lancer Counter-Strike 2 (avec l'option -insecure).
    echo.
)

native\mesa_injector.exe native\mesa_bridge.dll
set INJ_CODE=%ERRORLEVEL%

echo.
if %INJ_CODE% equ 0 (
    echo [SUCCES] DLL injectee avec succes dans cs2.exe.
) else if %INJ_CODE% equ 2 (
    echo [ERREUR] cs2.exe non trouve en memoire.
) else (
    echo [ERREUR] Echec de l'injection (Code de retour : %INJ_CODE%).
    echo Verifiez que le jeu tourne avec l'option -insecure et sans privilege administrateur conflictuel.
)

echo.
pause
