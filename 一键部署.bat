@echo off
chcp 65001 >nul
cd /d "%~dp0"
python deploy.py
if errorlevel 1 (
    echo.
    echo [提示] 如果上面显示找不到 python，请先安装 Python：https://www.python.org/downloads/
    echo 安装时记得勾选 "Add Python to PATH"
    pause
)
