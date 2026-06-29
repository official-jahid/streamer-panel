# Flask Web Application for REGIX Studio

## Description
Flask patterns for building the REGIX Studio gaming panel web interface.

## Project Structure

```
templates/
├── base.html           # Blood theme base template
└── partials/           # Reusable Jinja2 components

static/
└── js/                 # JavaScript for interactivity
```

## Quick Start

```python
from flask import Flask, jsonify, render_template, request

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', user=user)

@app.post('/auth')
def auth():
    data = request.get_json()
    # Authentication logic
    return jsonify(status=200, message="success")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4070, threaded=True)
```

## Blood Theme CSS

```css
.blood-gradient {
    background: linear-gradient(135deg, #000000, #2D0000, #8B0000);
}

.neon-blood {
    color: #FF6B6B;
    text-shadow: 0 0 10px #DC143C, 0 0 20px #FF0000;
}

.button-blood {
    background: linear-gradient(45deg, #2D0000, #8B0000);
    transition: all 0.3s ease;
}
```

## Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | Homepage/Login |
| GET | `/dashboard` | Main interface |
| GET | `/sniper-panel` | Sniper mode |
| GET | `/extra-panel` | Extra features |
| GET | `/settings` | User settings |
| POST | `/auth` | Login |
| POST | `/aimbot-on` | Enable aimbot |
| POST | `/aimbot-off` | Disable aimbot |

## References
- REGIX Studio app.py for full endpoint implementation
- templates/base.html for theme configuration