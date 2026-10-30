@echo off
cd /d "%~dp0"
chcp 65001 >nul
title ARCEUS // GITHUB DEPLOYMENT PIPELINE
echo ===============================================================
echo   ARCEUS // PREPARATION ET PUSH GITHUB
echo ===============================================================
echo.
echo [1/4] Verification du repository distant...
git remote -v
echo.
echo [2/4] Indexation des fichiers (git add)...
git add .
echo.
echo [3/4] Creation du commit officiel...
git commit -m "feat(arceus): release v3.0 - cloud supabase auth, standalone player exe, storefront and admin back-office"
echo.
echo [4/4] Push vers GitHub (origin main)...
git push -u origin main
echo.
if %ERRORLEVEL% EQU 0 (
    echo ===============================================================
    echo   [SUCCES] Tout a ete pousse sur GitHub avec succes !
    echo ===============================================================
) else (
    echo ===============================================================
    echo   [INFO] Si GitHub demande vos identifiants, connectez-vous
    echo   dans la fenetre d'authentification Git.
    echo ===============================================================
)
echo.
pause
