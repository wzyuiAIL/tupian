@echo off
chcp 65001 >nul
title AI Product Image Generator - One Click Start

echo.
echo ====================================
echo   AI Product Image Generator
echo   One Click Start
echo ====================================
echo.

REM Check if portable Python exists
if not exist "python_portable\python.exe" (
    echo [ERROR] Portable Python not found!
    echo.
    echo Please download Portable Python:
    echo https://www.python.org/ftp/python/3.12.0/python-3.12.0-embed-amd64.zip
    echo.
    echo Extract and rename to: python_portable
    echo Place in current directory
    echo.
    pause
    exit /b 1
)

REM Check if assets folder exists
if not exist "assets\web_sdk_index.html" (
    echo [ERROR] Assets folder or web_sdk_index.html not found!
    echo.
    echo Please ensure correct structure:
    echo.
    echo ai_product_image_generator/
    echo ├── python_portable/
    echo ├── assets/
    echo │   └── web_sdk_index.html
    echo └── start_with_portable_python.bat
    echo.
    pause
    exit /b 1
)

echo [Step 1/3] Starting Portable Python...
echo.

REM Start server
cd assets
..\python_portable\python.exe -m http.server 8080

REM Server stopped
echo.
echo Server stopped!
pause
