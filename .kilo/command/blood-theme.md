# Blood Theme Development Commands

## Usage
Use these commands to work with REGIX Studio project.

---

## `/setup` - Install dependencies and run setup

Installs all required packages for REGIX Studio development.

```bash
pip install -r requirements.txt
pip install flask pymem keyauth-client pyinstaller
```

---

## `/dev` - Run development server

Starts Flask development server on port 4070.

```bash
python app.py
```

Server runs at `http://localhost:4070`

---

## `/build` - Build executable

Creates Windows executable using PyInstaller.

```bash
pyinstaller REGIX_Studio.spec --noconsole --onefile
```

Output: `dist/REGIX_Studio.exe`

---

## `/test-memory` - Test memory module

Runs memory manipulation tests without launching UI.

```bash
python -c "from Memory import *; print('Memory module loaded')"
```