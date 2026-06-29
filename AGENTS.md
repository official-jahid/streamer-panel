# AGENTS.md - REGIX Studio

## Project Overview

REGIX Studio is a gaming enhancement panel built with:
- **Backend**: Flask (Python)
- **Frontend**: Jinja2 templates with Tailwind CSS
- **Memory**: PyMem for Windows memory manipulation
- **Auth**: KeyAuth integration

## Quick Start for Agents

```bash
# Setup
pip install -r requirements.txt

# Run
python app.py

# Build
pyinstaller REGIX_Studio.spec
```

## Project Structure

```
streamer-panel/
├── app.py              # Main Flask application with API endpoints
├── Memory.py           # Memory manipulation, AimbotAI, AOB patterns
├── utils.py            # Process utilities
├── keyauth.py          # KeyAuth authentication wrapper
├── requirements.txt    # Python dependencies
├── templates/          # Blood-themed Jinja2 HTML templates
│   ├── base.html      # Base template with blood theme
│   └── partials/      # Reusable components
└── static/
    └── js/            # JavaScript with blood-red effects
```

## Key Functions

### Memory Operations (Memory.py)
- `aimbot_load()` - Scan for aimbot addresses
- `aimbot_on(addresses)` - Enable aimbot
- `aimbot_off(addresses)` - Disable aimbot
- `drag_load()` - Scan for drag addresses
- `aimdrag_on/off()` - Enable/disable drag
- `AimbotAI.work()` - Start silent aim thread
- `AimbotAI.stop()` - Stop silent aim thread

### Flask API Endpoints
- `GET /` - Homepage
- `GET /dashboard` - Main dashboard
- `POST /auth` - Login authentication
- `POST /aimbot-on` - Enable aimbot
- `POST /aimbot-off` - Disable aimbot

## Configuration

Configure in `app.py`:
```python
keyauthapp = api(
    name = "REGIX Studio",
    ownerid = "GIgun4Td7t",
    secret = "your-secret-key",
    version = "1.0",
    hash_to_check = getchecksum()
)
```

## Blood Theme Colors

- Primary: `#8B0000` (Dark Red)
- Secondary: `#DC143C` (Crimson)
- Accent: `#FF0000` (Red)
- Background: `#000000 → #2D0000 → #8B0000`
- Text: `#FF6B6B` (Light Red)

---

*Made with 🩸 by REGIX Studio Team*