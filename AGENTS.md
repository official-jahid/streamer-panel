# AGENTS.md — Project Guide for AI Agents

This file provides essential context for AI agents (like Cline) working on this project. Read this before making any changes.

## Project Overview

**Project:** REGIX Studio (formerly AXC Corporation) — Streamer Panel
**Type:** Python Flask web application packaged as a Windows EXE
**Purpose:** A streamer control panel with game enhancement features (aimbot, chams, ESP, sniper tools) for FreeFire running on BlueStacks emulator (HD-Player.exe)

## Branding

| Old (AXC)       | New (REGIX)               |
| --------------- | ------------------------- |
| AXC             | REGIX                     |
| AXC CORPORATION | REGIX Studio              |
| AXC_Streamer    | Microsoft Edge (EXE name) |
| AXC_Corp        | REGIX_Studio              |
| AXC_Corporation | REGIX                     |

**IMPORTANT:** Never reintroduce "AXC" branding. All branding must use REGIX / REGIX Studio.

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
│   └── js/                # Frontend JavaScript files
├── templates/             # Flask HTML templates
│   ├── base.html          # Base template (title: REGIX Studio)
│   ├── homepage.html      # Login page
│   ├── dashboard.html     # Main dashboard
│   ├── sniper.html        # Sniper tools panel
│   ├── extra.html         # Extra features panel
│   ├── settings.html      # Settings panel
│   └── partials/          # Jinja partials/macros
└── build/                 # PyInstaller build artifacts (generated)
```

## Key Files & Their Roles

### app.py (Main Application)

- Flask app with routes for authentication, aimbot, chams, ESP, sniper tools
- Uses KeyAuth for license authentication
- Injects DLLs into HD-Player.exe (BlueStacks) using pyinjector
- Has anti-debug features (injects into Taskmgr.exe and ProcessHacker.exe)
- Runs on port 4070
- Sets AppUserModelID "REGIX.Studio" for taskbar icon

### Key Routes

| Route                | Method | Purpose                                        |
| -------------------- | ------ | ---------------------------------------------- |
| `/`                  | GET    | Homepage (redirects to dashboard if logged in) |
| `/dashboard`         | GET    | Main dashboard                                 |
| `/auth`              | POST   | Login authentication                           |
| `/auth-check`        | POST   | Check auth status                              |
| `/logout`            | GET    | Logout                                         |
| `/logs`              | POST   | Get message logs                               |
| `/user-info`         | POST   | Get user info                                  |
| `/get-process`       | POST   | Check HD-Player.exe process                    |
| `/aimbot-load`       | POST   | Load aimbot                                    |
| `/aimbot-on`         | POST   | Enable aimbot                                  |
| `/aimbot-off`        | POST   | Disable aimbot                                 |
| `/aimdrag-load`      | POST   | Load aim drag                                  |
| `/aimdrag-on`        | POST   | Enable aim drag                                |
| `/aimdrag-off`       | POST   | Disable aim drag                               |
| `/chams-menu`        | POST   | Inject chams menu DLL                          |
| `/chams-3D`          | POST   | Inject wallhack DLL                            |
| `/update-bit32`      | POST   | Select 32-bit mode                             |
| `/update-bit64`      | POST   | Select 64-bit mode                             |
| `/sniper-scope-on`   | POST   | Enable sniper scope                            |
| `/sniper-scope-off`  | POST   | Disable sniper scope                           |
| `/sniper-switch-on`  | POST   | Enable sniper switch                           |
| `/sniper-switch-off` | POST   | Disable sniper switch                          |
| `/m82b-esp-on`       | POST   | Enable M82B ESP                                |
| `/m82b-esp-off`      | POST   | Disable M82B ESP                               |
| `/sniper-panel`      | GET    | Sniper panel page                              |
| `/extra-panel`       | GET    | Extra panel page                               |
| `/settings`          | GET    | Settings page                                  |

### Spec Files (PyInstaller)

| Spec File             | EXE Name           | Icon     |
| --------------------- | ------------------ | -------- |
| `Microsoft_Edge.spec` | Microsoft Edge.exe | logo.ico |
| `REGIX_Studio.spec`   | REGIX_Studio.exe   | logo.ico |
| `REGIX.spec`          | REGIX.exe          | logo.ico |
| `app.spec`            | app.exe            | logo.ico |
| `svchost.spec`        | svchost.exe        | logo.ico |
| `service maker.spec`  | Service Maker.exe  | —        |
| `service worker.spec` | Service Worker.exe | —        |

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

### Install Dependencies

```bat
python -m pip install -r requirements.txt
```

## KeyAuth Configuration

The app uses KeyAuth for license authentication. Credentials are in `app.py`:

```python
keyauthapp = api(
    name="Streamer Panel",
    ownerid="fcJpSzqmdT",
    secret="2ce120135d10373c502963876896b4bbc65e5f04d3149d5695c837d6c4cda2b6",
    version="1.0",
    hash_to_check=getchecksum()
)
```

## Important Notes for AI Agents

1. **Never overwrite app.py entirely** — it's 424 lines with critical game memory manipulation code. Use targeted `replace_in_file` edits instead.
2. **The build script is named `Buld.bat`** (intentional misspelling) — don't "fix" it.
3. **DLL injection targets:** HD-Player.exe (game), Taskmgr.exe (anti-debug), ProcessHacker.exe (anti-debug)
4. **The app hides from taskbar** using `hide_from_taskbar()` and hides console window
5. **Port 4070** is the Flask server port
6. **logo.ico** is the EXE icon — always reference it in spec files
7. **VS Code Local History** at `%APPDATA%\Code\User\History\` can recover accidentally overwritten files
8. **Never use `write_to_file` on app.py** — always use `replace_in_file` for targeted edits
9. **The `build/` directory** contains PyInstaller artifacts — safe to delete and regenerate
10. **`dist/` directory** contains built EXEs — generated by build process

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

## Dependencies (requirements.txt)

- Flask 3.0.3 — Web framework
- Werkzeug 3.0.3 — WSGI toolkit
- waitress 3.0.0 — Production WSGI server
- requests 2.32.3 — HTTP requests
- pymem 1.13.1 — Memory manipulation
- pyinjector 1.3.0 — DLL injection
- psutil 6.0.0 — Process/system utilities
- pywin32 311 — Windows API bindings
- pyinstaller 6.22.0 — EXE builder
- python-dotenv 1.0.1 — Environment variables
- pyyaml 6.0.2 — YAML parsing
- colorama 0.4.6 — Colored terminal output
- keyboard 0.13.5 — Keyboard input
- pynput 1.7.7 — Input monitoring
