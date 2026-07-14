@echo off
title AXC STREAMER — EXE BUILDER
echo ============================================
echo   AXC STREAMER — EXE BUILDER
echo ============================================
echo.

cd /d "%~dp0"

echo [1/4] Installing essential packages...
python -m pip install Flask werkzeug waitress requests pymem psutil pyinjector pywin32 pyinstaller python-dotenv pyyaml colorama keyboard pynput

echo [2/4] Building EXE...
python -m PyInstaller --onefile --noconsole --name "AXC_Streamer" --add-data "templates;templates" --add-data "static;static" --add-data "dlls;dlls" --hidden-import=pymem --hidden-import=psutil --hidden-import=pyinjector --hidden-import=flask --hidden-import=waitress --hidden-import=keyauth --hidden-import=Memory --hidden-import=utils app.py

if exist "dist\AXC_Streamer.exe" (
    echo [3/3] ✅ Build successful!
    echo EXE Location: dist\AXC_Streamer.exe
) else (
    echo ❌ Build failed.
)

pause