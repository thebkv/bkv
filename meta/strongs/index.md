---
title: "Strong's Concordance"
permalink: /meta/strongs/
---

# Strong's Concordance

Look up the Hebrew and Greek words indexed in *Strong's Exhaustive Concordance*.

Search by **Strong's number**, **English transliteration**, **original Hebrew or Greek**, or a word in the definition.

<input
  type="search"
  id="strongs-search"
  placeholder="Try G26, agape, love, H85, Abraham..."
  autocomplete="off"
  style="width:100%;max-width:700px;padding:14px 16px;font-size:18px;margin:20px 0 8px;"
>

<div id="strongs-status" style="margin-bottom:1.5rem;"></div>

<div id="strongs-results"></div>

<script>
const search = document.getElementById('strongs-search');
const status = document.getElementById('strongs-status');
const results = document.getElementById('strongs-results');

let entries = [];
let byNumber = new Map();

function escapeHtml(value) {
  return String(value ?? '')
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}

function normalizeStrongNumber(value) {
  const q = value.trim().toUpperCase().replace(/\s+/g, '');

  if (/^[GH]\d+$/.test(q)) {
    const prefix = q[0];
    const number = parseInt(q.slice(1), 10);
    return prefix + number;
  }

  return null;
}

function makeReferencesClickable(text) {
  const safe = escapeHtml(text);

  return safe.replace(/\b([GH])(\d{1,4})\b/g, (match, prefix, digits) => {
    const number = prefix + parseInt(digits, 10);

    if (!byNumber.has(number)) return match;

    return `<button
      type="button"
      class="strongs-ref"
      data-strongs="${number}"
      style="background:none;border:0;padding:0;color:#58a6ff;text-decoration:underline;cursor:pointer;font:inherit;"
    >${number}</button>`;
  });
}

function renderEntry(entry) {
  const language = entry.number.startsWith('H') ? 'Hebrew' : 'Greek';

  return `
    <article style="border:1px solid #26344d;border-radius:9px;padding:1.25rem 1.4rem;margin:0 0 1rem;">
      
      <div style="display:flex;gap:.8rem;align-items:baseline;flex-wrap:wrap;">
        <h2 style="margin:0;">${escapeHtml(entry.number)}</h2>
        <span style="opacity:.7;">${language}</span>
      </div>

      <div style="font-size:2rem;margin:.8rem 0 .35rem;">
        ${escapeHtml(entry.lemma)}
      </div>

      ${entry.xlit ? `
        <div style="font-size:1.15rem;">
          <strong>Transliteration:</strong> ${escapeHtml(entry.xlit)}
        </div>
      ` : ''}

      ${entry.pronounce ? `
        <div style="margin-top:.25rem;">
          <strong>Pronunciation:</strong> ${escapeHtml(entry.pronounce)}
        </div>
      ` : ''}

      ${entry.description ? `
        <div style="margin-top:1rem;line-height:1.65;">
          ${makeReferencesClickable(entry.description)}
        </div>
      ` : `
        <div style="margin-top:1rem;opacity:.7;">
          No definition supplied in this edition.
        </div>
      `}

    </article>
  `;
}

function showEntry(number, updateUrl = true) {
  const normalized = normalizeStrongNumber(number);
  const entry = normalized ? byNumber.get(normalized) : null;

  if (!entry) return;

  search.value = normalized;
  status.innerHTML = '';
  results.innerHTML = renderEntry(entry);

  if (updateUrl) {
    const url = new URL(window.location.href);
    url.searchParams.set('q', normalized);
    history.replaceState({}, '', url);
  }

  window.scrollTo({
    top: search.getBoundingClientRect().top + window.scrollY - 30,
    behavior: 'smooth'
  });
}

function runSearch(query) {
  const q = query.trim();

  if (!q) {
    results.innerHTML = '';
    status.innerHTML =
      `<p>${entries.length.toLocaleString()} Strong's entries available — ` +
      `8,674 Hebrew and 5,624 Greek.</p>`;

    const url = new URL(window.location.href);
    url.searchParams.delete('q');
    history.replaceState({}, '', url);

    return;
  }

  const exactNumber = normalizeStrongNumber(q);

  if (exactNumber && byNumber.has(exactNumber)) {
    showEntry(exactNumber);
    return;
  }

  const lower = q.toLowerCase();

  const matches = entries
    .filter(entry =>
      entry.number.toLowerCase().includes(lower) ||
      (entry.xlit || '').toLowerCase().includes(lower) ||
      (entry.pronounce || '').toLowerCase().includes(lower) ||
      (entry.lemma || '').toLowerCase().includes(lower) ||
      (entry.description || '').toLowerCase().includes(lower)
    )
    .slice(0, 50);

  if (!matches.length) {
    status.innerHTML = '<p>No matching Strong\'s entries.</p>';
    results.innerHTML = '';
    return;
  }

  status.innerHTML =
    `<p>${matches.length}${matches.length === 50 ? '+' : ''} matching entries.</p>`;

  results.innerHTML = matches.map(renderEntry).join('');

  const url = new URL(window.location.href);
  url.searchParams.set('q', q);
  history.replaceState({}, '', url);
}

status.innerHTML = '<p>Loading Strong\'s Concordance…</p>';

fetch('{{ "/meta/strongs/strongs.json" | relative_url }}')
  .then(response => {
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    return response.json();
  })
  .then(data => {
    entries = data;

    byNumber = new Map(
      entries.map(entry => [entry.number.toUpperCase(), entry])
    );

    const params = new URLSearchParams(window.location.search);
    const initialQuery = params.get('q');

    if (initialQuery) {
      search.value = initialQuery;
      runSearch(initialQuery);
    } else {
      status.innerHTML =
        `<p>${entries.length.toLocaleString()} Strong's entries available — ` +
        `8,674 Hebrew and 5,624 Greek.</p>`;
    }
  })
  .catch(error => {
    console.error(error);
    status.innerHTML =
      '<p><strong>Strong\'s data could not be loaded.</strong></p>';
  });

search.addEventListener('input', function () {
  runSearch(this.value);
});

results.addEventListener('click', function (event) {
  const button = event.target.closest('.strongs-ref');

  if (!button) return;

  showEntry(button.dataset.strongs);
});
</script>

---

[← Reference Library]({{ '/meta/' | relative_url }})
