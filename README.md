# REGIX Studio — Streamer Panel

A streamer control panel with game enhancement features for FreeFire running on BlueStacks emulator (HD-Player.exe). Built with Python Flask and packaged as a Windows EXE.

> **Formerly known as AXC Corporation** — fully rebranded to **REGIX Studio**.

---

## Features

- 🔐 **License Authentication** — KeyAuth-based license system
- 🎯 **Aimbot** — Load, enable, and disable aimbot
- 🎯 **Aim Drag** — Load, enable, and disable aim drag
- 👁️ **Chams** — Chams menu and 3D wallhack injection
- 🔭 **Sniper Tools** — Sniper scope and switch (32/64-bit support)
- 📡 **M82B ESP** — Enable/disable M82B ESP
- 🛡️ **Anti-Debug** — Auto-injects into Taskmgr.exe and ProcessHacker.exe
- 🖥️ **Web Dashboard** — Full control panel accessible via browser
- 📟 **Live Console** — Real-time operation logs in the web UI

---

## Requirements

- **Windows 10/11**
- **Python 3.7+** (only needed for development/building)
- **BlueStacks emulator** running the game (`HD-Player.exe`)
- A **KeyAuth** application (for license authentication)

---

## Quick Start

### 1. Install Dependencies

```bat
python -m pip install -r requirements.txt
```

> `Buld.bat` also installs all dependencies automatically, so you can skip this
> step if you are building the EXE.

### 2. Run in Development Mode

```bat
python app.py
```

Then open **http://localhost:4070** in your browser.

> The app hides its console window and starts a Flask server on port `4070`.
> Leave the script running — it also starts background threads that watch for
> `Taskmgr.exe` / `ProcessHacker.exe` (anti-debug) and handle DLL injection.

---

## Building the EXE

### Method 1: Build Script (Recommended)

```bat
Buld.bat
```

This script will:

1. Install all required Python packages.
2. Run PyInstaller with the correct flags.
3. Output the EXE to `dist\Microsoft Edge.exe`.

### Method 2: Direct PyInstaller Command

```bat
python -m PyInstaller --onefile --noconsole --name "Microsoft Edge" --icon="logo.ico" --add-data "templates;templates" --add-data "static;static" --add-data "dlls;dlls" --hidden-import=pymem --hidden-import=psutil --hidden-import=pyinjector --hidden-import=flask --hidden-import=waitress --hidden-import=keyauth --hidden-import=Memory --hidden-import=utils app.py
```

| Flag                               | Meaning                                     |
| ---------------------------------- | ------------------------------------------- |
| `--onefile`                        | Single-file EXE output                      |
| `--noconsole`                      | No console window at runtime                |
| `--name`                           | The resulting EXE file name                 |
| `--icon="logo.ico"`                | Sets the application icon                   |
| `--add-data "templates;templates"` | Bundles HTML/Jinja templates                |
| `--add-data "static;static"`       | Bundles frontend JS/logo                    |
| `--add-data "dlls;dlls"`           | Bundles the injection DLLs                  |
| `--hidden-import=...`              | Forces PyInstaller to include these modules |

### Method 3: Using a Spec File

```bat
python -m PyInstaller Microsoft_Edge.spec
```

Other spec files (see [Build Outputs](#build-outputs) below):

```bat
python -m PyInstaller REGIX_Studio.spec
python -m PyInstaller REGIX.spec
python -m PyInstaller app.spec
python -m PyInstaller svchost.spec
```

### Cleaning Build Artifacts

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
├── Buld.bat               # Build script (note: intentionally misspelled)
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

## API Routes

| Route                | Method | Purpose                                        |
| -------------------- | ------ | ---------------------------------------------- |
| `/`                  | GET    | Homepage (redirects to dashboard if logged in) |
| `/dashboard`         | GET    | Main dashboard (headshot/aimbot page)          |
| `/auth`              | POST   | Login authentication                           |
| `/auth-check`        | POST   | Check auth status                              |
| `/logout`            | GET    | Logout                                         |
| `/logs`              | POST   | Get console/log messages                       |
| `/user-info`         | POST   | Get user info (username, HWID, IP, expiry)     |
| `/get-process`       | POST   | Check `HD-Player.exe` process                  |
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

---

## Build Outputs

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

## Dependencies

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

## Customization Guide

Everything you can customize in this project, where to find it, and how to change it.

### 1. Branding / Application Name

| What                       | Where                                 | How                                                           |
| -------------------------- | ------------------------------------- | ------------------------------------------------------------- |
| **Browser tab title**      | `templates/base.html`                 | Change `<title>REGIX Studio</title>`                          |
| **Login page title text**  | `templates/homepage.html`             | Change `REGIX Studio` span under logo                         |
| **Dashboard welcome text** | `templates/partials/status.jinja`     | Edit `WELCOME TO REGIX STUDIO` and `DEV: REGIX ANMOL & ARPIT` |
| **EXE name**               | `Buld.bat` and spec files             | Change `--name "Microsoft Edge"`                              |
| **Taskbar AppUserModelID** | `app.py` line 17                      | `SetCurrentProcessExplicitAppUserModelID("REGIX.Studio")`     |
| **App icon**               | `logo.ico` + `static/images/logo.png` | Replace both files (keep exact filenames)                     |
| **Flask secret key**       | `app.py` line 53                      | `app.secret_key = 'your_new_secret_key_here'`                 |

### 2. KeyAuth License System

Location: `app.py` lines ~65–71

```python
keyauthapp = api(
    name="Your Application Name",
    ownerid="your_owner_id",
    secret="your_secret_key",
    version="1.0",
    hash_to_check=getchecksum()
)
```

| Field           | Where to get it                                         |
| --------------- | ------------------------------------------------------- |
| `name`          | KeyAuth Dashboard → Application name                    |
| `ownerid`       | KeyAuth Dashboard → Settings → Owner ID (10 chars)      |
| `secret`        | KeyAuth Dashboard → Settings → Secret (64 chars)        |
| `version`       | Must match the version set in KeyAuth dashboard         |
| `hash_to_check` | Leave as `getchecksum()` to lock the app to a file hash |

> If `ownerid`/`secret` lengths are wrong (ownerid ≠ 10, secret ≠ 64), the app
> prints a warning and exits. Full KeyAuth API methods are in `keyauth.py`.

### 3. Server Port & Network

Location: `app.py` line ~412

```python
app.run(debug=False, host='0.0.0.0', port=4070, threaded=True, use_reloader=False)
```

- **Port**: change `4070` to any free port.
- **host**:
  - `0.0.0.0` → accessible from any device on the LAN.
  - `127.0.0.1` → localhost only (more private).

### 4. Game / Emulator Process Target

| File                    | Variable                            | Default       | Purpose                                      |
| ----------------------- | ----------------------------------- | ------------- | -------------------------------------------- |
| `Memory.py`             | `Pymem("HD-Player.exe")`            | HD-Player.exe | Emulator process for memory manipulation     |
| `app.py` `/get-process` | `Memory.get_process`                | HD-Player.exe | Process presence check                       |
| `app.py` chams routes   | `get_pid('HD-Player.exe')`          | HD-Player.exe | DLL injection target                         |
| `app.py` 32/64-bit      | `is32bit = True`                    | 32-bit        | Default bit mode                             |
| `static/js/emulator.js` | `$("#btn1").addClass("active")`     | 32-bit        | Default highlight in UI                      |
| `app.py` anti-debug     | `Taskmgr.exe` / `ProcessHacker.exe` | —             | Processes that get injected with `alpha.dll` |
| `utils.py`              | `check_process(processName)`        | parameterized | Generic process checker                      |

To target a different emulator, replace **every** `"HD-Player.exe"` string
(with search-and-replace across `app.py`, `Memory.py`).

### 5. Feature ↔ DLL Mapping

Location: `app.py`

| Feature / Route            | DLL Path              | Notes                       |
| -------------------------- | --------------------- | --------------------------- |
| Chams Menu `/chams-menu`   | `dlls/FARHAN EXE.dll` | Injected into game process  |
| Chams 3D `/chams-3D`       | `dlls/wallhack.dll`   | Injected into game process  |
| Anti-Debug (Taskmgr)       | `dlls/alpha.dll`      | Injected into Taskmgr       |
| Anti-Debug (ProcessHacker) | `dlls/alpha.dll`      | Injected into ProcessHacker |

> **Important:** Only `wallhack.dll` is currently present in the `dlls/`
> directory. Replace the filenames with your own DLLs. Remember to re-build the
> EXE so the new DLLs get bundled via `--add-data "dlls;dlls"`.

### 6. Memory Pattern (AOB) Customization

| File        | Variable                                | Purpose                                  |
| ----------- | --------------------------------------- | ---------------------------------------- |
| `Memory.py` | `AIMBOT_PATTERN`                        | Byte pattern scanned for aimbot values   |
| `Memory.py` | `DRAG_PATTERN`                          | Byte pattern scanned for aim drag values |
| `Memory.py` | aimbot offsets `0xB4 / 0xB8 / 0xB2`     | Pointers for source/target value swap    |
| `Memory.py` | drag offsets `0xEB / 0xAB / 0xAE`       | Pointer offsets for drag feature         |
| `app.py`    | sniper scope `search`/`replace` bytes   | 32-bit & 64-bit patterns                 |
| `app.py`    | sniper switch `search1`/`replace` bytes | 32-bit & 64-bit patterns                 |
| `app.py`    | M82B ESP `search`/`replace` bytes       | 32-bit & 64-bit strings                  |

When the game updates these offsets/patterns, update them here. The
`mkp()` function in `Memory.py` converts `??` wildcards to scan masks.

### 7. UI Theme (Colors & Fonts)

The UI uses **Tailwind CSS (CDN)** + custom CSS in each partial. Accent color
is the teal-green `#1bbc9b`.

| Stylesheet Value                                   | Where                               | Current Color               |
| -------------------------------------------------- | ----------------------------------- | --------------------------- |
| Accent (borders, active)                           | All partials                        | `#1bbc9b` (teal)            |
| Panel background (`#status`, `#tabs`, `#headshot`) | partials                            | `#1f2427` (dark gray)       |
| Page background                                    | `dashboard.html` / `settings.html`  | `bg-slate-800` / `bg-black` |
| Active tab color                                   | `templates/partials/tabs.jinja`     | `#1bbc9b`                   |
| Inactive tab color                                 | `templates/partials/tabs.jinja`     | `#363a40`                   |
| Emulator active                                    | `templates/partials/emulator.jinja` | `#586fe4` (blue)            |
| Font family                                        | `base.html` + page bodies           | `monospace` / `font-mono`   |
| Console log text                                   | `static/js/console.js`              | `text-green-400 text-lg`    |

To re-theme: do a global search-and-replace of the hex colors across
`templates/` and `static/`. For example replace every `#1bbc9b` with your own
accent (e.g. `#ff5500`).

### 8. Feature Labels & Subtitles (Visible Text)

| Location                            | Current Labels                                           |
| ----------------------------------- | -------------------------------------------------------- |
| `templates/partials/headshot.jinja` | Aimbot Load, Aimbot, Aimbot Drag Load, Aimbot Drag       |
| `templates/partials/sniper.jinja`   | Sniper Scope, Sniper Switch                              |
| `templates/partials/extra.jinja`    | Chams Menu, Chams 3D, M82B ESP (+ commented Aim FOV row) |
| `templates/partials/settings.jinja` | Username, HWID, Expiry, Online Users                     |
| `templates/partials/status.jinja`   | Status, welcome message, version                         |
| `templates/partials/emulator.jinja` | Emulator, 32bit, 64bit                                   |
| `templates/partials/console.jinja`  | Console, Open/Close                                      |

Edit the `<h2>` / `<span>` text in each `.jinja` partial.

### 9. Page / Tab Configuration

| Page      | File                       | Tab #          | Component        |
| --------- | -------------------------- | -------------- | ---------------- |
| Dashboard | `templates/dashboard.html` | `Tabs.Tabs(1)` | Headshot partial |
| Sniper    | `templates/sniper.html`    | `Tabs.Tabs(2)` | Sniper partial   |
| Extra     | `templates/extra.html`     | `Tabs.Tabs(3)` | Extra partial    |
| Settings  | `templates/settings.html`  | `Tabs.Tabs(4)` | Settings partial |

The actual tab buttons are defined in `templates/partials/tabs.jinja`.
To add a new page: copy an existing page/partial, attach an ID in
`tabs.jinja`, and create the Flask route + JS file.

### 10. Version Number & Console Logs

| Value                                         | File                   | Line                |
| --------------------------------------------- | ---------------------- | ------------------- |
| `version = "1.0"`                             | `app.py`               | ~81                 |
| Dashboard passes `version=keyauthapp.version` | `app.py`               | `/dashboard`        |
| Console messages (`"... Aimbot Load Done"`)   | `app.py`               | Every route         |
| Console log styling                           | `static/js/console.js` | GREEN / OPEN styles |

Change the version string for a new release — it shows in the status bar next
to the version badge.

### 11. Build Configuration

| What           | File                    | Change                                 |
| -------------- | ----------------------- | -------------------------------------- |
| EXE name       | `Buld.bat` / spec files | `--name "Your Panel Name"`             |
| Icon           | `Buld.bat` / spec files | `--icon="youricon.ico"`                |
| Bundled assets | `Buld.bat`              | Edit `--add-data` entries              |
| Hidden imports | `Buld.bat`              | Add/remove `--hidden-import=...` flags |
| Build script   | `Buld.bat`              | Python packages, PyInstaller flags     |

### 12. Hardcoded Log Messages

Every feature route appends a message to the console log. Change the text in
`app.py` if you want custom notifications. For example:

```python
messages.append(datetime.datetime.now().strftime("%H:%M:%S") + " Aimbot Load Done")
```

---

## Troubleshooting

| Problem                         | Possible Fix                                                  |
| ------------------------------- | ------------------------------------------------------------- |
| `KeyAuth_Invalid` on startup    | Your KeyAuth ownerID/secret/name don't match                  |
| "Credentials Mismatch" on login | Wrong KeyAuth user/password, or version mismatch              |
| No process found                | Start BlueStacks first, keep game running                     |
| Aimbot Load fails               | Pattern changed — update `AIMBOT_PATTERN` in `Memory.py`      |
| DLL injection fails             | Ensure `dlls/` is bundled at build time (`--add-data`)        |
| Port already in use             | Change port in `app.py`                                       |
| EXE detected by antivirus       | Rebuild with different `--name`; submit false-positive report |

---

## License

This project is for authorized use only. Unauthorized distribution or use is prohibited.

---

**REGIX Studio** — All rights reserved.
