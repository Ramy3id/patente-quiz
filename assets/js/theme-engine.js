/**
 * Patente B Pro - Universal Theme Engine (Light / Dark Mode)
 * Features:
 * - Zero FOUC (Flash of Unstyled Content) execution
 * - LocalStorage persistence across all portal pages
 * - Smooth transition animations
 * - Accessible keyboard shortcut [Alt + T]
 */

(function () {
  const THEME_KEY = 'patente_theme';

  // 1. Instant execution to set class on <html> before paint
  function getPreferredTheme() {
    const saved = localStorage.getItem(THEME_KEY);
    if (saved === 'light' || saved === 'dark') return saved;
    // Default to dark mode for Patente B Pro
    return 'dark';
  }

  const currentTheme = getPreferredTheme();
  const html = document.documentElement;

  if (currentTheme === 'light') {
    html.classList.remove('dark');
    html.classList.add('light');
  } else {
    html.classList.remove('light');
    html.classList.add('dark');
  }

  // 2. Public API functions
  window.applyTheme = function (theme) {
    if (theme === 'light') {
      html.classList.remove('dark');
      html.classList.add('light');
    } else {
      html.classList.remove('light');
      html.classList.add('dark');
    }
    localStorage.setItem(THEME_KEY, theme);
    updateThemeButtons(theme);
  };

  window.toggleTheme = function () {
    const isLight = html.classList.contains('light');
    const nextTheme = isLight ? 'dark' : 'light';
    window.applyTheme(nextTheme);

    // Audio feedback if sound engine exists
    if (typeof playSound === 'function') {
      playSound('click');
    } else if (window.soundEngine && typeof window.soundEngine.click === 'function') {
      window.soundEngine.click();
    }
  };

  function updateThemeButtons(theme) {
    const icons = document.querySelectorAll('.theme-icon-span, #themeIcon');
    const labels = document.querySelectorAll('.theme-label-span, #themeLabel');

    icons.forEach(icon => {
      icon.textContent = theme === 'light' ? '🌙' : '☀️';
    });

    labels.forEach(label => {
      label.textContent = theme === 'light' ? 'الوضع الليلي' : 'الوضع النهاري';
    });
  }

  // 3. Setup listeners once DOM is ready
  document.addEventListener('DOMContentLoaded', () => {
    updateThemeButtons(html.classList.contains('light') ? 'light' : 'dark');

    // Keyboard shortcut: Alt + T or T (when not typing in inputs)
    document.addEventListener('keydown', (e) => {
      if (['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement.tagName)) return;
      if (e.key === 't' || e.key === 'T' || (e.altKey && (e.key === 't' || e.key === 'T'))) {
        window.toggleTheme();
      }
    });
  });
})();
