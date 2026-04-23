@echo off
chcp 65001 >nul
echo ============================================================
echo 🚀 启动 CORS 代理服务器
echo ============================================================
echo.

:: 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误：未检测到 Python
    echo.
    echo 请先安装 Python：
    echo 1. 访问 https://www.python.org/downloads/
    echo 2. 下载并安装 Python 3.9 或更高版本
    echo 3. 安装时务必勾选 "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

echo ✅ 检测到 Python

:: 检查requests库
python -c "import requests" >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  正在安装 requests 库...
    pip install requests
    if %errorlevel% neq 0 (
        echo ❌ 安装失败，请手动执行：pip install requests
        pause
        exit /b 1
    )
)

echo ✅ 依赖库已就绪
echo.

:: 检查代理服务器文件
if not exist "%~dp0cors_proxy_server.py" (
    echo ❌ 错误：找不到 cors_proxy_server.py 文件
    echo 请确保此脚本与 cors_proxy_server.py 在同一目录下
    echo.
    pause
    exit /b 1
)

echo ✅ 代理服务器文件已找到
echo.
echo ============================================================
echo 🚀 正在启动代理服务器...
echo ============================================================
echo.

:: 启动代理服务器
python "%~dp0cors_proxy_server.py"

pause
