/* Shell behaviour shared by every page: theme, navigation, flashes, toasts. */
(function () {
  'use strict';

  const root = document.documentElement;
  const body = document.body;

  /* ---------- theme ---------- */

  const STORAGE_KEY = 'gridwatch-theme';

  function currentTheme() {
    if (root.dataset.theme) return root.dataset.theme;
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  function paintThemeToggle() {
    const dark = currentTheme() === 'dark';
    document.querySelectorAll('[data-theme-icon]').forEach((el) => {
      el.hidden = (el.dataset.themeIcon === 'light') === dark;
    });
  }

  document.querySelectorAll('[data-theme-toggle]').forEach((button) => {
    button.addEventListener('click', () => {
      const next = currentTheme() === 'dark' ? 'light' : 'dark';
      root.dataset.theme = next;
      try { localStorage.setItem(STORAGE_KEY, next); } catch (e) { /* private mode */ }
      paintThemeToggle();
      document.dispatchEvent(new CustomEvent('gridwatch:themechange', { detail: { theme: next } }));
    });
  });
  paintThemeToggle();

  /* ---------- mobile navigation ---------- */

  function closeNav() { body.classList.remove('nav-open'); }

  document.querySelectorAll('[data-nav-toggle]').forEach((button) => {
    button.addEventListener('click', () => body.classList.toggle('nav-open'));
  });
  document.querySelectorAll('[data-nav-close]').forEach((el) => el.addEventListener('click', closeNav));
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') closeNav();
  });

  /* ---------- flash messages ---------- */

  document.querySelectorAll('[data-dismiss]').forEach((button) => {
    button.addEventListener('click', () => button.closest('.flash')?.remove());
  });

  /* ---------- toasts ---------- */

  const ICONS = {
    success: '<path d="M20 6 9 17l-5-5"/>',
    error: '<circle cx="12" cy="12" r="9"/><path d="M12 8v4"/><path d="M12 16h.01"/>',
    info: '<circle cx="12" cy="12" r="9"/><path d="M12 16v-4"/><path d="M12 8h.01"/>',
  };

  function toast(message, kind = 'info', ttl = 5000) {
    const host = document.getElementById('toasts');
    if (!host) return;
    const el = document.createElement('div');
    el.className = `toast toast--${kind}`;
    el.setAttribute('role', kind === 'error' ? 'alert' : 'status');
    el.innerHTML =
      `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" ` +
      `stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${ICONS[kind] || ICONS.info}</svg>` +
      '<span></span>';
    el.lastElementChild.textContent = message;
    host.appendChild(el);
    setTimeout(() => el.remove(), ttl);
  }

  /* ---------- fetch helper ---------- */

  async function postJSON(url, payload) {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRF-Token': body.dataset.csrf || '',
      },
      body: JSON.stringify(payload),
    });
    let data = {};
    try { data = await response.json(); } catch (e) { /* non-JSON error page */ }
    if (!response.ok || data.ok === false) {
      throw new Error(data.error || `Request failed (${response.status})`);
    }
    return data;
  }

  async function getJSON(url) {
    const response = await fetch(url, { headers: { Accept: 'application/json' } });
    if (!response.ok) throw new Error(`Request failed (${response.status})`);
    return response.json();
  }

  /* ---------- relative timestamps ---------- */

  function relative(iso) {
    const then = Date.parse(iso);
    if (Number.isNaN(then)) return iso;
    const seconds = Math.round((Date.now() - then) / 1000);
    if (seconds < 60) return 'just now';
    const units = [['minute', 60], ['hour', 60], ['day', 24], ['month', 30], ['year', 12]];
    let value = seconds / 60;
    let unit = 'minute';
    for (let i = 0; i < units.length - 1; i += 1) {
      if (Math.abs(value) < units[i + 1][1]) { unit = units[i][0]; break; }
      value /= units[i + 1][1];
      unit = units[i + 1][0];
    }
    return new Intl.RelativeTimeFormat(undefined, { numeric: 'auto' })
      .format(-Math.round(value), unit);
  }

  function paintTimestamps(scope = document) {
    scope.querySelectorAll('[data-timestamp]').forEach((el) => {
      const iso = el.dataset.timestamp;
      if (!iso) return;
      el.textContent = relative(iso);
      el.title = new Date(iso).toLocaleString();
    });
  }
  paintTimestamps();
  setInterval(() => paintTimestamps(), 30000);

  /* ---------- login convenience ---------- */

  document.querySelectorAll('[data-fill-demo]').forEach((button) => {
    button.addEventListener('click', () => {
      const email = document.getElementById('email');
      const password = document.getElementById('password');
      if (email) email.value = button.dataset.email || '';
      if (password) password.value = button.dataset.password || '';
      password?.focus();
    });
  });

  window.GridWatch = Object.assign(window.GridWatch || {}, {
    toast, postJSON, getJSON, currentTheme, relative, paintTimestamps,
  });
})();
