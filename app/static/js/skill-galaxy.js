/* Skill Galaxy Canvas Animation */
(function() {
  var canvas = document.getElementById('skillGalaxy');
  if (!canvas) return;

  var ctx = canvas.getContext('2d');
  var particles = [];
  var animationId;

  // Get skills from DOM
  var skillElements = document.querySelectorAll('.skill-badge');
  var skills = Array.from(skillElements).map(el => ({
    name: el.textContent.trim(),
    x: Math.random() * canvas.width,
    y: Math.random() * canvas.height,
    vx: (Math.random() - 0.5) * 2,
    vy: (Math.random() - 0.5) * 2,
    radius: Math.random() * 3 + 2
  }));

  // Resize canvas to fill container
  function resizeCanvas() {
    var rect = canvas.parentElement.getBoundingClientRect();
    canvas.width = rect.width;
    canvas.height = rect.height;
  }

  // Initialize particles
  function init() {
    resizeCanvas();
    particles = skills.map(skill => ({
      ...skill,
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height
    }));
    animate();
  }

  // Animation loop
  function animate() {
    ctx.fillStyle = 'rgba(255, 255, 255, 0.05)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Draw particles
    particles.forEach(particle => {
      particle.x += particle.vx;
      particle.y += particle.vy;

      // Bounce off edges
      if (particle.x - particle.radius < 0 || particle.x + particle.radius > canvas.width) {
        particle.vx *= -1;
        particle.x = Math.max(particle.radius, Math.min(canvas.width - particle.radius, particle.x));
      }
      if (particle.y - particle.radius < 0 || particle.y + particle.radius > canvas.height) {
        particle.vy *= -1;
        particle.y = Math.max(particle.radius, Math.min(canvas.height - particle.radius, particle.y));
      }

      // Draw particle
      ctx.fillStyle = '#667eea';
      ctx.beginPath();
      ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
      ctx.fill();

      // Draw label
      ctx.fillStyle = '#fff';
      ctx.font = '12px sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(particle.name.substring(0, 3), particle.x, particle.y);
    });

    // Draw connections between nearby particles
    for (var i = 0; i < particles.length; i++) {
      for (var j = i + 1; j < particles.length; j++) {
        var dx = particles[i].x - particles[j].x;
        var dy = particles[i].y - particles[j].y;
        var dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < 150) {
          ctx.strokeStyle = `rgba(102, 126, 234, ${0.3 * (1 - dist / 150)})`;
          ctx.lineWidth = 1;
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.stroke();
        }
      }
    }

    animationId = requestAnimationFrame(animate);
  }

  // Start animation
  init();

  // Handle window resize
  window.addEventListener('resize', resizeCanvas);
})();
