/* Dashboard: send control commands and keep the cards in step with the grid. */
(function () {
  'use strict';

  const { toast, postJSON, getJSON, paintTimestamps } = window.GridWatch;
  const container = document.getElementById('appliances');
  if (!container) return;

  const pollSeconds = Number(document.body.dataset.poll || 20);
  let inFlight = false;

  function cardFor(name) {
    return container.querySelector(`[data-appliance="${CSS.escape(name)}"]`);
  }

  function paintCard(appliance) {
    const card = cardFor(appliance.name);
    if (!card) return;

    card.classList.toggle('is-on', Boolean(appliance.power));

    const labels = {
      'power-label': appliance.powerLabel,
      'speed-label': appliance.speedLabel,
      'direction-label': appliance.directionLabel,
    };
    Object.entries(labels).forEach(([role, value]) => {
      const el = card.querySelector(`[data-role="${role}"]`);
      if (el && value) el.textContent = value;
    });

    // Readings are derived from the new state server-side, so replace them
    // rather than leaving the pre-command values on screen.
    const readings = card.querySelector('[data-role="readings"]');
    if (readings) {
      readings.replaceChildren(...appliance.readings.map((reading) => {
        const item = document.createElement('div');
        item.className = 'readout__item';
        const term = document.createElement('dt');
        term.textContent = reading.metric === 'temperature' ? 'Temp' : 'Current';
        const value = document.createElement('dd');
        value.append(String(reading.value));
        const unit = document.createElement('span');
        unit.className = 'unit small muted';
        unit.textContent = reading.metric === 'temperature' ? ' \u00b0C' : ' mA';
        value.append(unit);
        item.append(term, value);
        return item;
      }));
    }

    const badge = card.querySelector('[data-role="health-badge"]');
    if (badge && appliance.healthLabel) {
      badge.className = `badge badge--${appliance.healthStatus}`;
      badge.lastChild.textContent = ` ${appliance.healthLabel} `;
    }

    card.querySelectorAll('.segmented[data-control]').forEach((group) => {
      const active = appliance[group.dataset.control];
      group.querySelectorAll('button').forEach((button) => {
        button.setAttribute('aria-pressed', String(Number(button.dataset.value) === active));
      });
    });
  }

  function paintStats(snapshot) {
    const set = (key, text) => {
      const el = document.querySelector(`[data-stat="${key}"]`);
      if (el) el.textContent = text;
    };
    const total = document.querySelector('[data-stat="active"]');
    if (total) {
      total.innerHTML = '';
      total.append(String(snapshot.activeCount));
      const unit = document.createElement('span');
      unit.className = 'unit';
      unit.textContent = `of ${snapshot.appliances.length}`;
      total.append(unit);
    }
    set('current', `${snapshot.totalCurrent} mA`);
    set('health', snapshot.overallHealth === null ? '--' : `${snapshot.overallHealth}%`);

    const updated = document.querySelector('[data-stat="updated"]');
    if (updated && snapshot.updatedAt) {
      updated.dataset.timestamp = snapshot.updatedAt;
      paintTimestamps(document);
    }

    const badge = document.querySelector('[data-unseen-count]');
    if (badge && typeof snapshot.unseenNotifications === 'number') {
      badge.textContent = String(snapshot.unseenNotifications);
      badge.hidden = snapshot.unseenNotifications === 0;
    }
  }

  function paint(snapshot) {
    snapshot.appliances.forEach(paintCard);
    paintStats(snapshot);
  }

  container.addEventListener('click', async (event) => {
    const button = event.target.closest('.segmented[data-control] button');
    if (!button || inFlight) return;

    const group = button.closest('.segmented');
    const card = button.closest('[data-appliance]');
    const payload = {
      appliance: card.dataset.appliance,
      control: group.dataset.control,
      value: Number(button.dataset.value),
    };
    if (button.getAttribute('aria-pressed') === 'true') return;

    inFlight = true;
    group.classList.add('is-busy');
    try {
      const data = await postJSON('/api/control', payload);
      paint(data.snapshot);
      if (data.delivered.length) {
        toast(data.delivered[0], 'success');
      }
      // A refusal is normal here: the OM2M gateway is often offline and
      // ThingSpeak throttles writes. Say so rather than failing silently.
      if (!data.delivered.length && data.refused.length) {
        toast(`Applied locally. ${data.refused.join('. ')}`, 'info', 7000);
      }
    } catch (error) {
      toast(error.message, 'error', 7000);
    } finally {
      group.classList.remove('is-busy');
      inFlight = false;
    }
  });

  async function refresh() {
    if (inFlight || document.hidden) return;
    try {
      const data = await getJSON('/api/snapshot');
      if (data.ok) paint(data.snapshot);
    } catch (error) {
      /* A failed poll is not worth interrupting the user for. */
    }
  }

  document.querySelectorAll('[data-refresh]').forEach((button) => {
    button.addEventListener('click', async () => {
      button.disabled = true;
      await refresh();
      button.disabled = false;
      toast('Grid state refreshed', 'success', 2500);
    });
  });

  setInterval(refresh, Math.max(5, pollSeconds) * 1000);
  document.addEventListener('visibilitychange', () => { if (!document.hidden) refresh(); });
})();
