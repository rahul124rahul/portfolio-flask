/* Main JavaScript */

// ─── Auto-dismiss flash alerts ───
document.addEventListener('DOMContentLoaded', function() {
  var alerts = document.querySelectorAll('.alert-dismissible');
  alerts.forEach(function(alert) {
    setTimeout(function() {
      var closeBtn = alert.querySelector('.btn-close');
      if (closeBtn) closeBtn.click();
    }, 5000);
  });
});


// ─── Dark Mode Toggle ───
(function() {
  var toggle = document.getElementById('darkModeToggle');
  var icon = document.getElementById('darkModeIcon');
  var html = document.documentElement;

  var stored = localStorage.getItem('theme');
  var prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  var theme = stored || (prefersDark ? 'dark' : 'light');

  html.setAttribute('data-bs-theme', theme);
  updateIcon(theme);

  if (toggle) {
    toggle.addEventListener('click', function() {
      var current = html.getAttribute('data-bs-theme');
      var next = current === 'dark' ? 'light' : 'dark';
      html.setAttribute('data-bs-theme', next);
      localStorage.setItem('theme', next);
      updateIcon(next);
    });
  }

  function updateIcon(t) {
    if (icon) {
      icon.className = t === 'dark' ? 'bi bi-sun-fill' : 'bi bi-moon-fill';
    }
  }
})();


// ─── Page Loader ───
window.addEventListener('load', function() {
  var loader = document.getElementById('pageLoader');
  if (loader) {
    loader.style.opacity = '0';
    setTimeout(function() { loader.style.display = 'none'; }, 500);
  }
});


// ─── Parallax Effect ───
window.addEventListener('scroll', function() {
  var hero = document.querySelector('.hero-section');
  if (hero) {
    var scrolled = window.pageYOffset;
    hero.style.backgroundPositionY = scrolled * 0.4 + 'px';
  }
});


// ─── Skill Badge Animation ───
(function() {
  var skillObserver = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        var badges = entry.target.querySelectorAll('.skill-badge');
        badges.forEach(function(badge, i) {
          setTimeout(function() { badge.classList.add('visible'); }, i * 80);
        });
        skillObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.2 });

  document.addEventListener('DOMContentLoaded', function() {
    var skillsSection = document.getElementById('skills');
    if (skillsSection) {
      var badges = skillsSection.querySelectorAll('.skill-badge');
      badges.forEach(function(badge) { badge.classList.add('animate-in'); });
      skillObserver.observe(skillsSection);
    }
  });
})();


// ─── 3D Card Tilt Effect ───
(function() {
  var cards = document.querySelectorAll('.card-3d');

  cards.forEach(function(card) {
    card.addEventListener('mousemove', function(e) {
      var rect = this.getBoundingClientRect();
      var x = e.clientX - rect.left;
      var y = e.clientY - rect.top;

      var centerX = rect.width / 2;
      var centerY = rect.height / 2;

      var rotateX = ((y - centerY) / centerY) * 10;
      var rotateY = ((centerX - x) / centerX) * 10;

      this.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-8px)`;
    });

    card.addEventListener('mouseleave', function() {
      this.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) translateY(0)';
    });
  });
})();

