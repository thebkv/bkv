---
title: "Strong's Concordance"
permalink: /meta/strongs/
---

# Strong's Concordance

Look up the Hebrew and Greek words indexed in *Strong's Exhaustive Concordance*.

Search by **Strong's number, English transliteration, original Hebrew or Greek,** or a word in the definition.

<div id="strongs-app"></div>

<script>
(function () {

  const app = document.getElementById('strongs-app');

  const searchBox = document.createElement('input');
  searchBox.type = 'search';
  searchBox.placeholder = 'Loading Strong\'s data...';
  searchBox.autocomplete = 'off';
  searchBox.disabled = true;

  searchBox.style.width = '100%';
  searchBox.style.maxWidth = '700px';
  searchBox.style.padding = '14px 16px';
  searchBox.style.fontSize = '18px';
  searchBox.style.margin = '20px 0 8px';
  searchBox.style.boxSizing = 'border-box';

  const statusBox = document.createElement('div');
  const resultsBox = document.createElement('div');

  statusBox.innerHTML = '<p>Loading 14,298 Strong\'s entries...</p>';

  app.appendChild(searchBox);
  app.appendChild(statusBox);
  app.appendChild(resultsBox);

  let entries = [];
  let ready = false;

  function escapeHtml(value) {
    return String(value || '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  function renderEntry(entry) {

    const language =
      entry.number.startsWith('H') ? 'Hebrew' : 'Greek';

    return `
      <div style="
        border:1px solid #26344d;
        border-radius:9px;
        padding:1.25rem 1.4rem;
        margin:1rem 0;
      ">

        <div style="font-size:1.5rem;font-weight:bold;">
          ${escapeHtml(entry.number)}
          <span style="
            font-size:1rem;
            font-weight:normal;
            opacity:.65;
            margin-left:.5rem;
          ">
            ${language}
          </span>
        </div>

        <div style="font-size:2rem;margin:.75rem 0;">
          ${escapeHtml(entry.lemma)}
        </div>

        ${entry.xlit ? `
          <p>
            <strong>Transliteration:</strong>
            ${escapeHtml(entry.xlit)}
          </p>
        ` : ''}

        ${entry.pronounce ? `
          <p>
            <strong>Pronunciation:</strong>
            ${escapeHtml(entry.pronounce)}
          </p>
        ` : ''}

        ${entry.description ? `
          <p style="line-height:1.65;">
            ${escapeHtml(entry.description)}
          </p>
        ` : ''}

      </div>
    `;
  }

  function searchEntries() {

    if (!ready) {
      return;
    }

    const query = searchBox.value.trim().toLowerCase();

    if (!query) {
      resultsBox.innerHTML = '';

      statusBox.innerHTML =
        `<p>${entries.length.toLocaleString()} entries available — ` +
        `8,674 Hebrew and 5,624 Greek.</p>`;

      return;
    }

    let normalizedNumber = query.toUpperCase();

    if (/^[GH]0*\d+$/.test(normalizedNumber)) {
      normalizedNumber =
        normalizedNumber.charAt(0) +
        parseInt(normalizedNumber.slice(1), 10);
    }

    const matches = [];

    for (const entry of entries) {

      const number = String(entry.number || '');
      const lemma = String(entry.lemma || '').toLowerCase();
      const xlit = String(entry.xlit || '').toLowerCase();
      const pronounce = String(entry.pronounce || '').toLowerCase();
      const description =
        String(entry.description || '').toLowerCase();

      if (
        number.toUpperCase() === normalizedNumber ||
        number.toLowerCase().includes(query) ||
        lemma.includes(query) ||
        xlit.includes(query) ||
        pronounce.includes(query) ||
        description.includes(query)
      ) {
        matches.push(entry);
      }

      if (matches.length >= 50) {
        break;
      }
    }

    if (matches.length === 0) {

      statusBox.innerHTML =
        `<p>No matching Strong's entries for <strong>` +
        `${escapeHtml(searchBox.value)}</strong>.</p>`;

      resultsBox.innerHTML = '';

      return;
    }

    statusBox.innerHTML =
      `<p>${matches.length}` +
      `${matches.length === 50 ? '+' : ''} matching entries.</p>`;

    resultsBox.innerHTML =
      matches.map(renderEntry).join('');
  }

  fetch('{{ "/meta/strongs/strongs.json" | relative_url }}')
    .then(function(response) {

      if (!response.ok) {
        throw new Error('HTTP ' + response.status);
      }

      return response.json();
    })
    .then(function(data) {

      if (!Array.isArray(data)) {
        throw new Error('Strong\'s JSON is not an array.');
      }

      entries = data;
      ready = true;

      searchBox.disabled = false;
      searchBox.placeholder =
        'Try sword, love, Abraham, agape, H2719, G26...';

      statusBox.innerHTML =
        `<p><strong>${entries.length.toLocaleString()}</strong> ` +
        `entries loaded — 8,674 Hebrew and 5,624 Greek.</p>`;

      const params =
        new URLSearchParams(window.location.search);

      const initialQuery = params.get('q');

      if (initialQuery) {
        searchBox.value = initialQuery;
        searchEntries();
      }

    })
    .catch(function(error) {

      console.error(error);

      searchBox.disabled = true;

      statusBox.innerHTML =
        `<p><strong>Strong's data could not be loaded.</strong> ` +
        `${escapeHtml(error.message)}</p>`;

    });

  searchBox.addEventListener('input', searchEntries);

})();
</script>

---

[← Reference Library]({{ '/meta/' | relative_url }})
