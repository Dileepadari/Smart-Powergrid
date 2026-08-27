/* Chart.js setup. Colours come from the CSS custom properties so the charts
   follow the page theme instead of carrying a second palette. */
(function () {
  'use strict';

  const charts = new Map();

  function token(name, fallback) {
    const value = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
    return value || fallback;
  }

  function palette() {
    return {
      ink: token('--ink', '#0b0b0b'),
      secondary: token('--ink-secondary', '#52514e'),
      muted: token('--ink-muted', '#898781'),
      grid: token('--gridline', '#e1e0d9'),
      surface: token('--surface', '#fcfcfb'),
      raised: token('--surface-raised', '#ffffff'),
      border: token('--border-strong', 'rgba(11,11,11,0.18)'),
      status: {
        3: token('--good', '#0ca30c'),
        2: token('--warning', '#fab219'),
        1: token('--critical', '#d03b3b'),
      },
      // Fixed categorical order: never cycled, never reassigned by rank.
      series: [1, 2, 3, 4, 5, 6].map((n) => token(`--series-${n}`, '#2a78d6')),
    };
  }

  function baseOptions(colors) {
    return {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: 'index', intersect: false },
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: colors.raised,
          titleColor: colors.ink,
          bodyColor: colors.secondary,
          borderColor: colors.border,
          borderWidth: 1,
          padding: 10,
          cornerRadius: 8,
          displayColors: true,
          boxWidth: 9,
          boxHeight: 9,
          boxPadding: 4,
          usePointStyle: true,
        },
      },
    };
  }

  function readJSON(id) {
    const node = document.getElementById(id);
    if (!node) return null;
    try { return JSON.parse(node.textContent); } catch (e) { return null; }
  }

  /* ---------- health: one bar per appliance, coloured by condition ---------- */

  function healthChart(canvasId, dataId) {
    const canvas = document.getElementById(canvasId);
    const payload = readJSON(dataId);
    if (!canvas || !payload) return;

    const appliances = Array.isArray(payload) ? payload : payload.appliances || [];
    const scored = appliances.filter((a) => a.health);
    if (!scored.length) return;

    const build = () => {
      const colors = palette();
      const chart = new Chart(canvas, {
        type: 'bar',
        data: {
          labels: scored.map((a) => a.label),
          datasets: [{
            label: 'Condition',
            data: scored.map((a) => a.health),
            backgroundColor: scored.map((a) => colors.status[a.health]),
            borderRadius: 4,
            borderSkipped: 'bottom',
            barPercentage: 0.5,
            categoryPercentage: 0.7,
            maxBarThickness: 42,
          }],
        },
        options: Object.assign(baseOptions(colors), {
          plugins: Object.assign(baseOptions(colors).plugins, {
            tooltip: Object.assign(baseOptions(colors).plugins.tooltip, {
              callbacks: {
                label: (item) => {
                  const a = scored[item.dataIndex];
                  return ` ${a.healthLabel} (${a.health}/3) - ${a.powerLabel}`;
                },
              },
            }),
          }),
          scales: {
            x: {
              grid: { display: false },
              border: { color: colors.grid },
              ticks: { color: colors.secondary, font: { size: 12 } },
            },
            y: {
              min: 0,
              max: 3,
              grid: { color: colors.grid, drawTicks: false },
              border: { display: false },
              ticks: {
                stepSize: 1,
                color: colors.muted,
                font: { size: 12 },
                callback: (value) => ({ 0: '', 1: 'Poor', 2: 'Fair', 3: 'Good' }[value] ?? ''),
              },
            },
          },
        }),
      });
      charts.set(canvasId, chart);
    };

    build();
    onThemeChange(canvasId, build);
  }

  /* ---------- statistics: current draw per appliance over time ---------- */

  function seriesChart(canvasId, seriesId, applianceId) {
    const canvas = document.getElementById(canvasId);
    const series = readJSON(seriesId);
    const snapshot = readJSON(applianceId);
    if (!canvas || !series || !snapshot) return;

    const appliances = snapshot.appliances.filter((a) => (series[a.name] || []).length);
    if (!appliances.length) return;

    const labels = (series[appliances[0].name] || []).map((point) =>
      new Date(point.t).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }));

    const build = () => {
      const colors = palette();
      const chart = new Chart(canvas, {
        type: 'line',
        data: {
          labels,
          datasets: appliances.map((a, index) => {
            const color = colors.series[index % colors.series.length];
            return {
              label: a.label,
              data: (series[a.name] || []).map((point) => point.v),
              borderColor: color,
              backgroundColor: color,
              borderWidth: 2,
              pointRadius: 0,
              pointHoverRadius: 5,
              pointHoverBorderWidth: 2,
              pointHoverBorderColor: colors.surface,
              tension: 0.28,
              spanGaps: true,
            };
          }),
        },
        options: Object.assign(baseOptions(colors), {
          plugins: Object.assign(baseOptions(colors).plugins, {
            legend: {
              display: true,
              position: 'bottom',
              align: 'start',
              labels: {
                color: colors.secondary,
                usePointStyle: true,
                pointStyle: 'rectRounded',
                boxWidth: 11,
                boxHeight: 11,
                padding: 16,
                font: { size: 12 },
              },
            },
            tooltip: Object.assign(baseOptions(colors).plugins.tooltip, {
              callbacks: { label: (item) => ` ${item.dataset.label}: ${item.formattedValue} mA` },
            }),
          }),
          scales: {
            x: {
              grid: { display: false },
              border: { color: colors.grid },
              ticks: { color: colors.muted, font: { size: 11 }, maxRotation: 0, autoSkipPadding: 24 },
            },
            y: {
              beginAtZero: true,
              grid: { color: colors.grid, drawTicks: false },
              border: { display: false },
              ticks: {
                color: colors.muted,
                font: { size: 11 },
                callback: (value) => `${value} mA`,
              },
            },
          },
        }),
      });
      charts.set(canvasId, chart);
    };

    build();
    onThemeChange(canvasId, build);
  }

  function onThemeChange(canvasId, rebuild) {
    document.addEventListener('gridwatch:themechange', () => {
      charts.get(canvasId)?.destroy();
      rebuild();
    });
  }

  window.GridWatch = Object.assign(window.GridWatch || {}, { healthChart, seriesChart });
})();
