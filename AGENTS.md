# AGENTS.md — Project Guide for AI Agents

This file provides essential context for AI agents (like Cline) working on this project. Read this before making any changes.

## Project Overview

**Project:** REGIX Studio (formerly AXC Corporation) — Streamer Panel
**Type:** Python Flask web application packaged as a Windows EXE
**Purpose:** A streamer control panel with game enhancement features (aimbot, chams, ESP, sniper tools) for FreeFire running on BlueStacks emulator (HD-Player.exe)

## Branding

| REGIX                     |
| ------------------------- |
| REGIX                     |
| REGIX Studio              |
| Microsoft Edge (EXE name) |
| REGIX_Studio              |
| REGIX                     |

**IMPORTANT:** Never reintroduce "AXC" branding. All branding must use REGIX / REGIX Studio.

---

## Install Dependencies

```bat
python -m pip install -r requirements.txt
```

Or install individually:

```bat
python -m pip install Flask werkzeug waitress requests pymem psutil pyinjector pywin32 pyinstaller python-dotenv pyyaml colorama keyboard pynput
```

## Build Commands

### Method 1: Build Script (Recommended)

```bat
Buld.bat
```

This installs dependencies and builds `dist\Microsoft Edge.exe`.

### Method 2: Direct PyInstaller

```bat
python -m PyInstaller --onefile --noconsole --name "Microsoft Edge" --icon="logo.ico" --add-data "templates;templates" --add-data "static;static" --add-data "dlls;dlls" --hidden-import=pymem --hidden-import=psutil --hidden-import=pyinjector --hidden-import=flask --hidden-import=waitress --hidden-import=keyauth --hidden-import=Memory --hidden-import=utils app.py
```

### Method 3: Using Spec File

```bat
python -m PyInstaller Microsoft_Edge.spec
```

### Run in Development Mode

```bat
python app.py
```

Then open http://localhost:4070 in a browser.

### Clean Build Artifacts

```bat
rmdir /s /q build dist
```

---

## Project Structure

```
streamer/
├── app.py                 # Main Flask application (entry point)
├── keyauth.py             # KeyAuth license authentication library
├── Memory.py              # Memory manipulation functions (pymem)
├── utils.py               # Utility functions (process checking)
├── test.py                # Test script
├── logo.ico               # Application icon (used for EXE)
├── requirements.txt       # Python dependencies
├── Buld.bat               # Build script (note: intentionally misspelled "Buld")
├── *.spec                 # PyInstaller build specifications
├── dlls/                  # DLL files for injection
│   └── wallhack.dll       # Wallhack DLL
├── static/
│   ├── images/logo.png    # Web logo
│   └── js/                # Frontend JavaScript files (per-page logic)
├── templates/             # Flask HTML templates
│   ├── base.html          # Base template (title: REGIX Studio)
│   ├── homepage.html      # Login page
│   ├── dashboard.html     # Headshot/Aimbot page (tab 1)
│   ├── sniper.html        # Sniper tools page (tab 2)
│   ├── extra.html         # Extra features page (tab 3)
│   ├── settings.html      # Settings page (tab 4)
│   └── partials/          # Jinja partials/macros (UI components)
└── build/                 # PyInstaller build artifacts (generated)
```

---

## Code Structure & Logic

### app.py (Main Application — 429 lines)

**Never overwrite app.py entirely.** Use targeted `replace_in_file` edits.

#### 1. Imports & Startup (lines 1–27)

```python
import os, sys, ctypes, datetime, threading, time, subprocess, pymem
from flask import Flask, jsonify, redirect, render_template, request, session
from keyauth import *
import Memory
from pyinjector import inject
import utils
```

- Sets `AppUserModelID` to `"REGIX.Studio"` for taskbar icon (line 17)
- Hides console window on Windows (lines 21–26)

#### 2. Process Hiding (lines 29–48)

```python
def hide_process():          # No-op placeholder (psutil)
def hide_from_taskbar():     # Uses win32gui to set WS_EX_TOOLWINDOW
```

#### 3. Flask App & KeyAuth (lines 52–71)

```python
app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'regix_studio_secure_key_2024'   # ← CHANGE for security

def getchecksum():  # MD5 hash of the running EXE for KeyAuth hash lock

keyauthapp = api(
    name="",        # ← YOUR KeyAuth application name
    ownerid="",     # ← YOUR KeyAuth owner ID (10 chars)
    secret="",      # ← YOUR KeyAuth secret (64 chars)
    version="1.0",
    hash_to_check=getchecksum()
)
```

**To update KeyAuth credentials:** replace the empty `name`, `ownerid`, `secret` values.

#### 4. Global Variables (lines 73–81)

```python
messages = []          # Console log messages (appended by every route)
addresses = []         # Aimbot memory addresses
drag_addresses = []    # Aim drag memory addresses
user = {}              # Logged-in user data (username, hwid, ip, expiry)
is32bit = True         # Default bit mode (True=32-bit, False=64-bit)
isChangedDirectory = False
tab = 1
version = "1.0"        # ← CHANGE for new release
```

#### 5. Page Routes (lines 92–108)

```python
@app.get('/sniper-panel')   # → renders Sniper.html (tab 2)
@app.get('/extra-panel')    # → renders Extra.html (tab 3)
@app.get('/settings')       # → renders Settings.html (tab 4)
```

All check `keyauthapp.user_data.username` and redirect to `/` if not logged in.

#### 6. Auth Routes (lines 110–158)

| Route                | Logic                                                                            |
| -------------------- | -------------------------------------------------------------------------------- |
| `/auth` (POST)       | Calls `keyauthapp.login()`, stores user data in `user` dict, appends log message |
| `/auth-check` (POST) | Returns 200 if `user` dict is non-empty, else 302                                |
| `/logout` (GET)      | Calls `keyauthapp.logout()`                                                      |
| `/logs` (POST)       | Returns `messages` reversed (newest first)                                       |
| `/user-info` (POST)  | Returns username, IP, HWID, expiry, online users via `keyauthapp.fetchOnline()`  |

#### 7. Process Check (lines 160–165)

```python
@app.post('/get-process')
def getProcess():
    status = Memory.get_process("HD-Player.exe")   # ← CHANGE process name
    if not status:
        return jsonify(status=303)
    return jsonify(status=200, pid=status)
```

#### 8. Aimbot Routes (lines 167–189)

```python
@app.post('/aimbot-load')   # → Memory.aimbot_load() → stores addresses
@app.post('/aimbot-on')     # → Memory.aimbot_on(addresses)
@app.post('/aimbot-off')    # → Memory.aimbot_off(addresses)
```

Each appends a timestamped message to `messages` and returns `jsonify(status=200)` or `304` on failure.

#### 9. Aim Drag Routes (lines 191–212)

```python
@app.post('/aimdrag-load')  # → Memory.drag_load() → stores drag_addresses
@app.post('/aimdrag-on')    # → Memory.aimdrag_on(drag_addresses)
@app.post('/aimdrag-off')   # → Memory.aimdrag_off(drag_addresses)
```

#### 10. Chams / DLL Injection Routes (lines 214–256)

```python
@app.post('/chams-menu')
def chamsMenu():
    pid = Memory.get_pid('HD-Player.exe')
    inject(pid, get_resource_path('dlls/FARHAN EXE.dll'))   # ← CHANGE DLL path
    # returns 200 on success, 305 on failure

@app.post('/chams-3D')
def chams3D():
    pid = Memory.get_pid('HD-Player.exe')
    inject(pid, get_resource_path('dlls/wallhack.dll'))     # ← CHANGE DLL path
```

#### 11. Bit Mode Routes (lines 229–241)

```python
@app.post('/update-bit32')   # → is32bit = True
@app.post('/update-bit64')   # → is32bit = False
```

#### 12. Sniper Scope Routes (lines 258–288)

Uses `Memory.scan_and_replace("HD-Player.exe", search, replace)` with 32-bit/64-bit byte patterns.

- **On:** searches for `search` pattern, writes `replace`
- **Off:** searches for `replace` pattern, writes `search` (reverses)

**To update patterns:** replace the `search`/`replace` byte strings in both `if not is32bit:` and `else:` branches.

#### 13. Sniper Switch Routes (lines 290–322)

Same pattern-swap logic as sniper scope, but uses two search patterns (`search1`, `search2`) for 32-bit mode.

#### 14. M82B ESP Routes (lines 324–354)

Swaps UTF-16 string patterns between `in-game/pickup/pickup_bm94` and `effects/vfx_in_game_laser_shop` for 32/64-bit.

#### 15. Home & Dashboard (lines 356–368)

```python
@app.get('/')            # → redirects to /dashboard if logged in, else Homepage.html
@app.get('/dashboard')   # → renders Dashboard.html with user + version
```

#### 16. Anti-Debug Threads (lines 372–403)

```python
def taskManager():      # Watches for Taskmgr.exe, injects dlls/alpha.dll
def processManager():   # Watches for ProcessHacker.exe, injects dlls/alpha.dll
```

Both run in a loop with `time.sleep(0.25)`, using `utils.check_process()` and `pymem.Pymem()`.

#### 17. Main Entry (lines 407–429)

```python
def run_flask():
    hide_from_taskbar()
    app.run(debug=False, host='0.0.0.0', port=4070, threaded=True, use_reloader=False)
    # host='0.0.0.0' = LAN accessible; '127.0.0.1' = localhost only
    # port=4070 ← CHANGE port here

if __name__ == "__main__":
    hide_process()
    flask_thread = threading.Thread(target=run_flask)
    task_thread = threading.Thread(target=taskManager)
    process_thread = threading.Thread(target=processManager)
    task_thread.start()
    process_thread.start()
    flask_thread.start()
    flask_thread.join()
    task_thread.join()
    process_thread.join()
```

---

### Memory.py (Memory Manipulation — 243 lines)

#### Key Functions

| Function                                         | Purpose                                            | Key Values to Update |
| ------------------------------------------------ | -------------------------------------------------- | -------------------- |
| `mkp(aob)`                                       | Converts AOB string with `??` wildcards to bytes   | —                    |
| `scan_and_replace(processName, search, replace)` | Scans process memory, writes replace bytes         | `processName`        |
| `get_process(procesName)`                        | Returns PID if process exists, else False          | `procesName`         |
| `get_pid(processName)`                           | Returns PID (raises if not found)                  | `processName`        |
| `get_drive_serial_number()`                      | Gets C: drive serial for HWID                      | —                    |
| `get_hwid()`                                     | Returns drive serial as HWID                       | —                    |
| `adjust_privileges()`                            | Enables SeDebugPrivilege for memory access         | —                    |
| `find_pattern(pm, module_name, pattern)`         | Scans for pattern, returns addresses               | —                    |
| `aimbot_load()`                                  | Scans `AIMBOT_PATTERN`, returns addresses          | `AIMBOT_PATTERN`     |
| `aimbot_on(addresses)`                           | Writes source value to target offset `0xB4`/`0xB8` | offsets              |
| `aimbot_off(addresses)`                          | Restores original values at offset `0xB2`          | offsets              |
| `drag_load()`                                    | Scans `DRAG_PATTERN`, returns addresses            | `DRAG_PATTERN`       |
| `aimdrag_on(drag_addresses)`                     | Writes at offsets `0xEB`/`0xAB`                    | offsets              |
| `aimdrag_off(drag_addresses)`                    | Restores at offset `0xAE`                          | offsets              |

#### AOB Patterns (lines 34–36)

```python
AIMBOT_PATTERN = "FF FF FF FF 00 00 ... 80 BF"   # ← UPDATE when game patches
DRAG_PATTERN  = "00 00 00 00 00 00 ... 80 BF"    # ← UPDATE when game patches
```

**To update patterns:** replace the hex string. `??` = wildcard byte.

#### Aimbot Offsets (lines 163–186)

```python
addressscan = address + 0xB8   # Source value location
addressrep  = address + 0xB4   # Target value location (write here)
# Off: addressrep = address + 0xB2  (restore original)
```

#### Drag Offsets (lines 219–240)

```python
addressscan = address + 0xEB   # Source value location
addressrep  = address + 0xAB   # Target value location (write here)
# Off: addressrep = address + 0xAE  (restore original)
```

---

### utils.py (Process Checking — 13 lines)

```python
import psutil

def check_process(processName):
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == processName:
            return True
    return False
```

Used by `taskManager()` and `processManager()` in app.py to detect anti-debug targets.

---

### keyauth.py (KeyAuth Library — 617 lines)

Standard KeyAuth Python library. The `api` class constructor:

```python
class api:
    def __init__(self, name, ownerid, secret, version, hash_to_check):
        # Validates ownerid (10 chars) and secret (64 chars)
        # Calls self.init() which sends an "init" request to KeyAuth
```

Key methods used by app.py:

- `login(user=..., password=...)` — returns True/False
- `logout()` — returns True/False
- `fetchOnline()` — returns list of online user dicts
- `user_data` — object with `.username`, `.hwid`, `.ip`, `.expires`

---

## Frontend Structure

### Templates (Jinja2)

| File             | Tab # | Partials Imported                         | Purpose                                                          |
| ---------------- | ----- | ----------------------------------------- | ---------------------------------------------------------------- |
| `base.html`      | —     | —                                         | Base layout, `<title>REGIX Studio</title>`, Tailwind CDN, jQuery |
| `homepage.html`  | —     | —                                         | Login page (username/password → `/auth`)                         |
| `dashboard.html` | 1     | Status, Emulator, Tabs, Headshot, Console | Aimbot/Headshot page                                             |
| `sniper.html`    | 2     | Status, Emulator, Tabs, Sniper, Console   | Sniper tools page                                                |
| `extra.html`     | 3     | Status, Emulator, Tabs, Extra, Console    | Extra features page                                              |
| `settings.html`  | 4     | Status, Emulator, Tabs, Settings, Console | Settings page                                                    |

### Partials (templates/partials/)

| File             | Macro             | UI Elements                                        | API Endpoints                                                                               |
| ---------------- | ----------------- | -------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| `status.jinja`   | `Status(version)` | Welcome text, online button, version badge         | `/get-process` (via status.js)                                                              |
| `emulator.jinja` | `Emulator()`      | 32bit/64bit selector                               | `/update-bit32`, `/update-bit64`                                                            |
| `tabs.jinja`     | `Tabs(num)`       | 4 tab buttons (Headshot/Sniper/Extra/Settings)     | —                                                                                           |
| `headshot.jinja` | `Headshot()`      | Aimbot Load, Aimbot, Aimbot Drag Load, Aimbot Drag | `/aimbot-load`, `/aimbot-on`, `/aimbot-off`, `/aimdrag-load`, `/aimdrag-on`, `/aimdrag-off` |
| `sniper.jinja`   | `Sniper()`        | Sniper Scope, Sniper Switch                        | `/sniper-scope-on/off`, `/sniper-switch-on/off`                                             |
| `extra.jinja`    | `Extra()`         | Chams Menu, Chams 3D, M82B ESP                     | `/chams-menu`, `/chams-3D`, `/m82b-esp-on/off`                                              |
| `settings.jinja` | `Settings()`      | Username, HWID, Expiry, Online Users               | `/user-info` (via settings.js)                                                              |
| `console.jinja`  | `Console()`       | Collapsible log panel                              | `/logs` (via console.js)                                                                    |

### JavaScript (static/js/)

| File          | Controls              | API Endpoints                                                                               |
| ------------- | --------------------- | ------------------------------------------------------------------------------------------- |
| `homepage.js` | Login form            | `/auth`                                                                                     |
| `status.js`   | Online/offline button | `/get-process`                                                                              |
| `emulator.js` | 32/64-bit buttons     | `/update-bit32`, `/update-bit64`                                                            |
| `headshot.js` | Aimbot + Drag buttons | `/aimbot-load`, `/aimbot-on`, `/aimbot-off`, `/aimdrag-load`, `/aimdrag-on`, `/aimdrag-off` |
| `sniper.js`   | Sniper buttons        | `/sniper-scope-on/off`, `/sniper-switch-on/off`                                             |
| `extra.js`    | Chams + M82B buttons  | `/chams-menu`, `/chams-3D`, `/m82b-esp-on/off`                                              |
| `settings.js` | User info display     | `/user-info`                                                                                |
| `console.js`  | Log panel             | `/logs`                                                                                     |

---

## UI Theme (Colors)

| Value                    | Where                              | Current                     |
| ------------------------ | ---------------------------------- | --------------------------- |
| Accent (borders, active) | All partials                       | `#1bbc9b` (teal)            |
| Panel background         | `#status`, `#tabs`, `#headshot`    | `#1f2427`                   |
| Page background          | `dashboard.html` / `settings.html` | `bg-slate-800` / `bg-black` |
| Inactive tab             | `tabs.jinja`                       | `#363a40`                   |
| Emulator active          | `emulator.jinja`                   | `#586fe4`                   |
| Font                     | `base.html` + pages                | `monospace` / `font-mono`   |

---

## KeyAuth Configuration

The app uses KeyAuth for license authentication. Credentials are in `app.py` (lines 65–71):

```python
keyauthapp = api(
    name="",        # ← Add your KeyAuth application name
    ownerid="",     # ← Add your KeyAuth application ownerid
    secret="",      # ← Add your KeyAuth application secret
    version="1.0",
    hash_to_check=getchecksum()
)
```

**To configure:** replace the empty strings with your KeyAuth dashboard values.

---

## Spec Files (PyInstaller)

| Spec File             | EXE Name           | Icon     |
| --------------------- | ------------------ | -------- |
| `Microsoft_Edge.spec` | Microsoft Edge.exe | logo.ico |
| `REGIX_Studio.spec`   | REGIX_Studio.exe   | logo.ico |
| `REGIX.spec`          | REGIX.exe          | logo.ico |
| `app.spec`            | app.exe            | logo.ico |
| `svchost.spec`        | svchost.exe        | logo.ico |
| `service maker.spec`  | Service Maker.exe  | —        |
| `service worker.spec` | Service Worker.exe | —        |

---

## Dependencies (requirements.txt)

| Package       | Version | Purpose                  |
| ------------- | ------- | ------------------------ |
| Flask         | 3.0.3   | Web framework            |
| Werkzeug      | 3.0.3   | WSGI toolkit             |
| waitress      | 3.0.0   | Production WSGI server   |
| requests      | 2.32.3  | HTTP requests (KeyAuth)  |
| pymem         | 1.13.1  | Memory manipulation      |
| pyinjector    | 1.3.0   | DLL injection            |
| psutil        | 6.0.0   | Process/system utilities |
| pywin32       | 311     | Windows API bindings     |
| pyinstaller   | 6.22.0  | EXE builder              |
| python-dotenv | 1.0.1   | Environment variables    |
| pyyaml        | 6.0.2   | YAML parsing             |
| colorama      | 0.4.6   | Colored terminal output  |
| keyboard      | 0.13.5  | Keyboard input           |
| pynput        | 1.7.7   | Input monitoring         |

---

## Important Notes for AI Agents

1. **Never overwrite app.py entirely** — it's 429 lines with critical game memory manipulation code. Use targeted `replace_in_file` edits instead.
2. **The build script is named `Buld.bat`** (intentional misspelling) — don't "fix" it.
3. **DLL injection targets:** HD-Player.exe (game), Taskmgr.exe (anti-debug), ProcessHacker.exe (anti-debug)
4. **The app hides from taskbar** using `hide_from_taskbar()` and hides console window
5. **Port 4070** is the Flask server port
6. **logo.ico** is the EXE icon — always reference it in spec files
7. **VS Code Local History** at `%APPDATA%\Code\User\History\` can recover accidentally overwritten files
8. **Never use `write_to_file` on app.py** — always use `replace_in_file` for targeted edits
9. **The `build/` directory** contains PyInstaller artifacts — safe to delete and regenerate
10. **`dist/` directory** contains built EXEs — generated by build process
11. **KeyAuth credentials are empty** in app.py — fill them in before running
12. **Only `wallhack.dll` ships** in `dlls/` — `FARHAN EXE.dll` and `alpha.dll` must be added before building
13. **Never reintroduce AXC branding** — always use REGIX / REGIX Studio

---

## Common Tasks

### Rebuild EXE after changes

```bat
Buld.bat
```

### Test the app locally (without building)

```bat
python app.py
```

Then open http://localhost:4070 in a browser.

### Clean build artifacts

```bat
rmdir /s /q build dist
```

### Update KeyAuth credentials

Edit `app.py` lines 65–71 — replace the empty `name`, `ownerid`, `secret` strings.

### Change the server port

Edit `app.py` line 412 — change `port=4070` to your desired port.

### Change the target process

Search-and-replace `"HD-Player.exe"` across `app.py` and `Memory.py`.

### Update memory patterns after a game patch

Edit `AIMBOT_PATTERN` and `DRAG_PATTERN` in `Memory.py` (lines 34–36), plus the sniper/M82B byte patterns in `app.py`.

### Change the EXE name

Edit `Buld.bat` — change `--name "Microsoft Edge"` to your desired name.

### Change the UI accent color

Search-and-replace `#1bbc9b` across `templates/` and `static/` with your new color.
