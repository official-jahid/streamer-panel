# Blood Theme UI for REGIX Studio

## Description
Blood-red themed user interface with animations and hover effects.

## Color Palette

| Name | Value | Usage |
|------|-------|-------|
| Primary | `#8B0000` | Dark red backgrounds |
| Secondary | `#DC143C` | Crimson accents |
| Accent | `#FF0000` | Red highlights |
| Background | `#000000 → #2D0000 → #8B0000` | page backgrounds |
| Text | `#FF6B6B` | Light red text |

## CSS Animations

```css
/* Blood glow pulsing effect */
@keyframes blood-glow {
    0%, 100% { box-shadow: 0 0 5px #8B0000, 0 0 10px #DC143C; }
    50% { box-shadow: 0 0 15px #FF0000, 0 0 25px #DC143C; }
}

.glow-effect {
    animation: blood-glow 2s infinite alternate;
}

/* Blood drip animation */
@keyframes blood-drip {
    0% { transform: translateY(-100%); opacity: 0; }
    100% { transform: translateY(0); opacity: 1; }
}

.blood-drip {
    animation: blood-drip 0.5s ease-out;
}

/* Button hover effects */
.button-blood:hover {
    transform: scale(1.05);
    filter: brightness(1.2);
}

/* Gradient background */
.blood-gradient {
    background: linear-gradient(135deg, #000000, #2D0000, #8B0000);
    min-height: 100vh;
}
```

## JavaScript Interactions

```javascript
// Blood splatter on click
function bloodSplatter(x, y) {
    const splatter = document.createElement('div');
    splatter.className = 'absolute w-4 h-4 bg-red-600 rounded-full animate-blood-drip';
    splatter.style.left = x + 'px';
    splatter.style.top = y + 'px';
    document.body.appendChild(splatter);
    setTimeout(() => splatter.remove(), 500);
}

// Neon flicker effect
function neonFlicker() {
    const elements = document.querySelectorAll('.neon-blood');
    elements.forEach(el => {
        el.style.textShadow = `0 0 ${Math.random() * 20}px #DC143C`;
    });
}
setInterval(neonFlicker, 100);
```

## Jinja2 Template Structure

```html
<!-- Inherit base template -->
{% extends "base.html" %}

<!-- Override content block -->
{% block content %}
<div class="blood-gradient min-h-screen">
    <h1 class="neon-blood text-4xl font-bold">{{ title }}</h1>
</div>
{% endblock %}
```

## References
- REGIX Studio templates/base.html
- REGIX Studio static/js/*.js files