@echo off
title GitHub Auto Sync - Patente B Pro
cls
echo ========================================================
echo   [1/3] Staging all files and audit updates...
echo ========================================================
cd /d "%~dp0"
git add -A

echo.
echo ========================================================
echo   [2/3] Committing changes...
echo ========================================================
git commit -m "feat: complete audit, translations fix, and mobile responsive update"

echo.
echo ========================================================
echo   [3/3] Uploading to GitHub...
echo ========================================================
git push origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================================
    echo   [SUCCESS] Uploaded successfully to GitHub!
    echo   Live site: https://ramy3id.github.io/patente-quiz/
    echo ========================================================
) else (
    echo.
    echo ========================================================
    echo   [ERROR] Push encountered an issue. Check connection.
    echo ========================================================
)

echo.
pause
