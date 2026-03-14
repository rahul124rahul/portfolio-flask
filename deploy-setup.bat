@echo off
REM Portfolio Deployment Setup Script (Windows)
REM This script initializes git, commits code, and pushes to GitHub

setlocal enabledelayedexpansion

set "GITHUB_USERNAME=rahul124rahul"
set "REPO_NAME=portfolio-flask"
set "GITHUB_TOKEN=%1"

if "!GITHUB_TOKEN!"=="" (
    echo Usage: deploy-setup.bat ^<github-token^>
    echo.
    echo Get your GitHub token from: https://github.com/settings/tokens
    exit /b 1
)

echo 🚀 Starting Portfolio Deployment Setup...
echo.

REM Initialize Git
echo 1️⃣ Initializing Git repository...
git init
git branch -M main
echo ✅ Git initialized
echo.

REM Add all files
echo 2️⃣ Staging all files...
git add .
echo ✅ Files staged
echo.

REM Create initial commit
echo 3️⃣ Creating initial commit...
git commit -m "Initial commit: Flask developer portfolio with advanced features"
echo ✅ Commit created
echo.

REM Add remote
echo 4️⃣ Adding remote repository...
git remote add origin "https://%GITHUB_USERNAME%:%GITHUB_TOKEN%@github.com/%GITHUB_USERNAME%/%REPO_NAME%.git"
echo ✅ Remote added
echo.

REM Push to GitHub
echo 5️⃣ Pushing to GitHub (this may take a moment)...
git push -u origin main
if errorlevel 1 (
    echo ❌ Push failed! Check your token and try again.
    exit /b 1
)
echo ✅ Code pushed to GitHub!
echo.

echo =========================================
echo ✨ Success! Your code is on GitHub ✨
echo =========================================
echo.
echo Next steps:
echo 1. Create Neon PostgreSQL account: https://neon.tech
echo 2. Create Render account: https://render.com
echo 3. Follow the DEPLOYMENT.md guide
echo.
echo Your repository: https://github.com/%GITHUB_USERNAME%/%REPO_NAME%
echo.

pause
