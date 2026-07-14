// Red Theme Particle Background
class ParticleBackground {
  constructor() {
    this.canvas = document.createElement("canvas");
    this.ctx = this.canvas.getContext("2d");
    this.particles = [];
    this.mouse = { x: null, y: null, radius: 120 };

    this.init();
  }

  init() {
    this.canvas.id = "particle-canvas";
    this.canvas.style.position = "fixed";
    this.canvas.style.top = "0";
    this.canvas.style.left = "0";
    this.canvas.style.width = "100vw";
    this.canvas.style.height = "100vh";
    this.canvas.style.zIndex = "0";
    this.canvas.style.pointerEvents = "none";

    document.body.prepend(this.canvas);

    this.resize();
    this.createParticles();
    this.animate();

    window.addEventListener("resize", () => this.resize());
    document.addEventListener("mousemove", (e) => this.handleMouse(e));
    document.addEventListener("mouseleave", () => this.handleMouseLeave());
  }

  resize() {
    this.canvas.width = window.innerWidth;
    this.canvas.height = window.innerHeight;
  }

  createParticles() {
    const particleCount = Math.min(
      120,
      Math.floor((this.canvas.width * this.canvas.height) / 8000),
    );

    for (let i = 0; i < particleCount; i++) {
      this.particles.push({
        x: Math.random() * this.canvas.width,
        y: Math.random() * this.canvas.height,
        radius: Math.random() * 2.5 + 1,
        speedX: (Math.random() - 0.5) * 0.5,
        speedY: -(Math.random() * 0.8 + 0.2),
        opacity: Math.random() * 0.6 + 0.2,
        pulse: Math.random() * Math.PI * 2,
        pulseSpeed: Math.random() * 0.02 + 0.01,
      });
    }
  }

  handleMouse(e) {
    this.mouse.x = e.clientX;
    this.mouse.y = e.clientY;
  }

  handleMouseLeave() {
    this.mouse.x = null;
    this.mouse.y = null;
  }

  animate() {
    const ctx = this.ctx;
    ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

    // Dark red gradient overlay for readability
    const gradient = ctx.createRadialGradient(
      this.canvas.width / 2,
      this.canvas.height / 2,
      0,
      this.canvas.width / 2,
      this.canvas.height / 2,
      Math.max(this.canvas.width, this.canvas.height) * 0.8,
    );
    gradient.addColorStop(0, "rgba(0, 0, 0, 0)");
    gradient.addColorStop(1, "rgba(5, 5, 10, 0.3)");
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

    // Red shades for particles
    const redShades = [
      "220, 38, 38", // red-600
      "185, 28, 28", // red-700
      "153, 27, 27", // red-800
      "127, 29, 29", // red-900
      "239, 68, 68", // red-500
    ];

    this.particles.forEach((p, index) => {
      // Update position
      p.x += p.speedX;
      p.y += p.speedY;

      // Pulse
      p.pulse += p.pulseSpeed;
      const currentOpacity = p.opacity * (0.7 + 0.3 * Math.sin(p.pulse));

      // Wrap around
      if (p.y < -10) {
        p.y = this.canvas.height + 10;
        p.x = Math.random() * this.canvas.width;
      }
      if (p.x < -10) p.x = this.canvas.width + 10;
      if (p.x > this.canvas.width + 10) p.x = -10;

      // Mouse repulsion
      if (this.mouse.x !== null && this.mouse.y !== null) {
        const dx = p.x - this.mouse.x;
        const dy = p.y - this.mouse.y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < this.mouse.radius) {
          const force = (this.mouse.radius - dist) / this.mouse.radius;
          const angle = Math.atan2(dy, dx);
          p.x += Math.cos(angle) * force * 2;
          p.y += Math.sin(angle) * force * 2;
        }
      }

      // Draw particle
      const shade = redShades[index % redShades.length];
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(${shade}, ${currentOpacity})`;
      ctx.fill();

      // Subtle glow for larger particles
      if (p.radius > 2) {
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.radius * 2.5, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(${shade}, ${currentOpacity * 0.15})`;
        ctx.fill();
      }

      // Draw connecting lines between nearby particles
      for (let j = index + 1; j < this.particles.length; j++) {
        const p2 = this.particles[j];
        const dx = p.x - p2.x;
        const dy = p.y - p2.y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < 120) {
          const lineOpacity = ((120 - dist) / 120) * 0.15;
          ctx.beginPath();
          ctx.moveTo(p.x, p.y);
          ctx.lineTo(p2.x, p2.y);
          ctx.strokeStyle = `rgba(220, 38, 38, ${lineOpacity})`;
          ctx.lineWidth = 0.5;
          ctx.stroke();
        }
      }
    });

    requestAnimationFrame(() => this.animate());
  }
}

// Initialize when DOM is ready
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", () => new ParticleBackground());
} else {
  new ParticleBackground();
}
