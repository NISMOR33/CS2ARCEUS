@echo off
setlocal enabledelayedexpansion
title ARCEUS // CS2 PREMIUM LAUNCHER

cd /d "%~dp0"

:menu
cls
echo =======================================================================
echo              ARCEUS // CS2 PREMIUM SUITE & SKIN CHANGER
echo =======================================================================
echo.
echo   --- TESTS SANS CS2 (SUR CE PC) ---
echo   [1] Lancer la Previsualisation Native DirectX11 (Menu ImGui Noir ^& Blanc)
echo   [2] Lancer l'Application Bureau ARCEUS (Catalogue complet SQLite 5 Mo)
echo   [3] Executer les Tests de Validation Scientifique (test_verification.py)
echo.
echo   --- LORSQUE CS2 EST DISPONIBLE ---
echo   [4] Injecter le Moteur Complet dans CS2 (Menu In-Game [Insert], Couteaux, Caisses)
echo   [5] Lancer CS2 en mode Insecure (-insecure -allow_third_party_software)
echo.
echo   [6] Quitter
echo.
echo =======================================================================
set /p choice="Selectionnez une option [1-6] : "

if "%choice%"=="1" goto launch_preview
if "%choice%"=="2" goto launch_desktop
if "%choice%"=="3" goto run_tests
if "%choice%"=="4" goto inject_engine
if "%choice%"=="5" goto launch_cs2
if "%choice%"=="6" exit /b 0
goto menu

:launch_preview
echo.
echo [ARCEUS] Lancement de la fenetre de previsualisation native DirectX 11...
start "" ARCEUS_Preview.exe
goto menu

:launch_desktop
echo.
echo [ARCEUS] Lancement de l'interface bureau complete...
start "" run_arceus.bat
goto menu

:run_tests
echo.
echo [ARCEUS] Execution de la suite de tests...
python test_verification.py
python compare_inspect_links.py
echo.
pause
goto menu

:inject_engine
echo.
echo [ARCEUS] Injection du moteur C++ dans CS2...
if exist "Lootline\x64\Release\ARCEUS.exe" (
    start "" "Lootline\x64\Release\ARCEUS.exe"
) else (
    echo [ERREUR] ARCEUS.exe introuvable dans Lootline\x64\Release.
    pause
)
goto menu

:launch_cs2
echo.
echo [ARCEUS] Lancement de Counter-Strike 2 via Steam en mode -insecure...
start steam://run/730//-insecure%20-allow_third_party_software/
goto menu
