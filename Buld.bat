@echo off
title REGIX STUDIO — EXE BUILDER
echo ============================================
echo   REGIX STUDIO — EXE BUILDER
echo ============================================
echo.

cd /d "%~dp0"

echo [1/4] Installing essential packages...
python -m pip install Flask werkzeug waitress requests pymem psutil pywin32 pyinstaller python-dotenv pyyaml colorama keyboard pynput

echo [2/4] Building EXE...
python -m PyInstaller --onefile --noconsole --name "Microsoft Edge" --icon="logo.ico" --add-data "templates;templates" --add-data "static;static" --add-data "dlls;dlls" --hidden-import=pymem --hidden-import=psutil --hidden-import=pyinjector --hidden-import=flask --hidden-import=waitress --hidden-import=keyauth --hidden-import=Memory --hidden-import=utils app.py

if exist "dist\Microsoft Edge.exe" (
    echo [3/3] ✅ Build successful!
    echo EXE Location: dist\Microsoft Edge.exe
) else (
    echo ❌ Build failed.
)

pause
