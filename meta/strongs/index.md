---
title: "Strong's Concordance"
permalink: /meta/strongs/
---

# Strong's Concordance

Look up the Hebrew and Greek words indexed in *Strong's Exhaustive Concordance*.

Search by **Strong's number, English transliteration, original Hebrew or Greek,** or a word in the definition.

<input type="search" id="strongs-search" placeholder="Try G26, agape, love, H85, Abraham..." autocomplete="off" style="width:100%;max-width:700px;padding:14px 16px;font-size:18px;margin:20px 0 8px;">

<div id="strongs-status">Loading Strong's data...</div>

<div id="strongs-results"></div>

<script>
(function () {

  const searchBox = document.getElementById('strongs-search');
  const statusBox = document.getElementById('strongs-status');
  const resultsBox = document.getElementById('strongs-results');

  let entries = [];

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
      entry.number && entry.number.charAt(0) === 'H'
        ? 'Hebrew'
        : 'Greek';

    return `
      <div style="border:1px solid #26344d;border-radius:9px;padding:1.25rem 1.4rem;margin:1rem 0;">

        <div style="font-size:1.5rem;font-weight:bold;">
          ${escapeHtml(entry.number)}
          <span style="font-size:1rem;font-weight:normal;opacity:.65;">
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

  function runSearch() {

    const query = searchBox.value.trim().toLowerCase();

    if (!query) {
      resultsBox.innerHTML = '';
      statusBox.innerHTML =
        entries.length.toLocaleString() + " Strong's entries available.";
      return;
    }

    let normalizedNumber = query.toUpperCase();

    if (/^[GH]0*\d+$/.test(normalizedNumber)) {
      normalizedNumber =
        normalizedNumber.charAt(0) +
        parseInt(normalizedNumber.substring(1), 10);
    }

    const matches = entries.filter(function(entry) {

      const number = (entry.number || '').toLowerCase();
      const lemma = (entry.lemma || '').toLowerCase();
      const xlit = (entry.xlit || '').toLowerCase();
      const pronounce = (entry.pronounce || '').toLowerCase();
      const description = (entry.description || '').toLowerCase();

      return (
        entry.number === normalizedNumber ||
        number.indexOf(query) !== -1 ||
        lemma.indexOf(query) !== -1 ||
        xlit.indexOf(query) !== -1 ||
        pronounce.indexOf(query) !== -1 ||
        description.indexOf(query) !== -1
      );

    }).slice(0, 50);

    if (!matches.length) {
      statusBox.innerHTML = "No matching Strong's entries.";
      resultsBox.innerHTML = '';
      return;
    }

    statusBox.innerHTML =
      matches.length +
      (matches.length === 50 ? '+' : '') +
      ' matching entries.';

    resultsBox.innerHTML =
      matches.map(renderEntry).join('');
  }

  fetch('{{ "/meta/strongs/strongs.json" | relative_url }}')
    .then(function(response) {

      if (!response.ok) {
        throw new Error(
          'Could not load strongs.json: HTTP ' + response.status
        );
      }

      return response.json();

    })
    .then(function(data) {

      if (!Array.isArray(data)) {
        throw new Error('strongs.json is not an array.');
      }

      entries = data;

      statusBox.innerHTML =
        entries.length.toLocaleString() +
        " Strong's entries available — 8,674 Hebrew and 5,624 Greek.";

      const params = new URLSearchParams(window.location.search);
      const initialQuery = params.get('q');

      if (initialQuery) {
        searchBox.value = initialQuery;
        runSearch();
      }

    })
    .catch(function(error) {

      console.error('Strong data error:', error);

      statusBox.innerHTML =
        "<strong>Strong's data could not be loaded.</strong>";

    });

  searchBox.addEventListener('input', runSearch);

})();
</script>

---

[← Reference Library]({{ '/meta/' | relative_url }})
