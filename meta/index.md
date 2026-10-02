---
title: "Reference Library"
permalink: /meta/
---

# Reference Library

Use these tools to follow names, places, words, symbols, structures, and recurring patterns across Scripture.

<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:1rem;margin:1.5rem 0 2.5rem;">

  <div style="border:1px solid #26344d;border-radius:9px;padding:1.2rem;">
    <h2 style="margin-top:0;">Names & Meanings</h2>
    <p>Look up biblical names, places, words, and their meanings.</p>

    <p>
      <a href="#bible-dictionary"><strong>Fillmore Bible Dictionary →</strong></a>
    </p>

    <p>
      <a href="#strongs-search-section"><strong>Strong's Hebrew & Greek →</strong></a>
    </p>

    <p style="margin-bottom:0;">
      <a href="#potts-search-section"><strong>Potts — Swedenborg Concordance →</strong></a>
    </p>
  </div>

  <div style="border:1px solid #26344d;border-radius:9px;padding:1.2rem;">
    <h2 style="margin-top:0;">The Biblical World</h2>
    <p>See how places and structures function in Scripture.</p>
    <p style="margin-bottom:0;">Tabernacle · Temple · Egypt to Canaan · Jerusalem · Wilderness</p>
  </div>

  <div style="border:1px solid #26344d;border-radius:9px;padding:1.2rem;">
    <h2 style="margin-top:0;">Fractal Patterns</h2>
    <p>Follow movements that repeat throughout Scripture and in the disciple.</p>
    <p>
      <a href="{{ '/fractals/younger-supplants-elder/' | relative_url }}"><strong>The Younger Supplants the Elder →</strong></a>
    </p>
    <p>Death and Resurrection · Exodus · Two Kings · Seed · Return <em>(coming later)</em></p>
    <p style="margin-bottom:0;">
      <a href="{{ '/fractals/' | relative_url }}"><strong>View all patterns →</strong></a>
    </p>
  </div>

  <div style="border:1px solid #26344d;border-radius:9px;padding:1.2rem;">
    <h2 style="margin-top:0;">Symbolics</h2>
    <p>Follow the recurring meaning of objects, people, places, and images across Scripture.</p>
    <p style="margin-bottom:0;">
      <a href="{{ '/symbolics/' | relative_url }}"><strong>Explore Biblical Symbolics →</strong></a>
    </p>
  </div>

  <div style="border:1px solid #26344d;border-radius:9px;padding:1.2rem;">
    <h2 style="margin-top:0;">How to Read</h2>
    <p>Simple principles for recognizing the interior meaning without losing the actual text.</p>
    <p style="margin-bottom:0;">Scripture interprets Scripture · Function before symbolism · The Savior Test · Selected insights from Fillmore, Swedenborg, Lamsa, and Nicoll</p>
  </div>

</div>

---

<h2 id="bible-dictionary">Fillmore Bible Dictionary</h2>

Search Charles Fillmore's <em>Metaphysical Bible Dictionary</em>.

<input type="search" id="fillmore-search" placeholder="Search a name, place, or term..." autocomplete="off" style="width:100%;max-width:700px;padding:14px 16px;font-size:18px;margin:20px 0 8px;">

<div id="fillmore-results"></div>

<script>
const fillmoreSearch = document.getElementById('fillmore-search');
const fillmoreResults = document.getElementById('fillmore-results');

let fillmoreEntries = [];

fillmoreResults.innerHTML = '<p>Loading Bible Dictionary…</p>';

fetch('{{ "/assets/data/fillmore-index.json" | relative_url }}')
  .then(response => {
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    return response.json();
  })
  .then(data => {
    fillmoreEntries = data;
    fillmoreResults.innerHTML =
      `<p>${fillmoreEntries.length.toLocaleString()} entries available.</p>`;
  })
  .catch(error => {
    console.error(error);
    fillmoreResults.innerHTML =
      '<p><strong>The Bible Dictionary could not be loaded.</strong></p>';
  });

fillmoreSearch.addEventListener('input', function () {
  const q = this.value.trim().toLowerCase();

  if (!q) {
    fillmoreResults.innerHTML =
      `<p>${fillmoreEntries.length.toLocaleString()} entries available.</p>`;
    return;
  }

  const matches = fillmoreEntries
    .filter(entry =>
      (entry.term || '').toLowerCase().includes(q)
    )
    .slice(0, 50);

  if (!matches.length) {
    fillmoreResults.innerHTML = '<p>No matching entries.</p>';
    return;
  }

  fillmoreResults.innerHTML = matches.map(entry =>
    `<p><a href="{{ site.baseurl }}${entry.url}">${entry.term}</a></p>`
  ).join('');
});
</script>

---

<h2 id="strongs-search-section">Strong's Hebrew & Greek</h2>

Look up the Hebrew and Greek words indexed in <em>Strong's Exhaustive Concordance</em>.

Search by <strong>Strong's number, English meaning, transliteration, original Hebrew or Greek,</strong> or a word in the definition.

<div id="strongs-app"></div>

<script>
(function () {
  var app = document.getElementById('strongs-app');

  var searchBox = document.createElement('input');
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

  var statusBox = document.createElement('div');
  var resultsBox = document.createElement('div');

  statusBox.innerHTML = '<p>Loading Strong\'s dictionary...</p>';

  app.appendChild(searchBox);
  app.appendChild(statusBox);
  app.appendChild(resultsBox);

  var entries = [];

  function escapeHtml(value) {
    return String(value || '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  function highlightSearch(text, query) {
    if (!text) return '';
    if (!query) return escapeHtml(text);
    var safeText = escapeHtml(text);
    var safeQuery = escapeHtml(query);
    var regexQuery = safeQuery.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    var regex = new RegExp('(' + regexQuery + ')', 'gi');
    return safeText.replace(regex,
      '<mark style="background:#f0b323;color:#0a1628;padding:0 .12em;border-radius:2px;">$1</mark>');
  }

  function renderEntry(entry, query) {
    var number = String(entry.number || '');
    var language = number.charAt(0) === 'H' ? 'Hebrew' : 'Greek';
    var lemma = String(entry.lemma || '');
    var english = String(entry.english || '');
    var description = String(entry.description || '');
    var searchHint = '';

    if (!english && query && description.toLowerCase().indexOf(query.toLowerCase()) !== -1) {
      searchHint = query;
    }

    var html = '<div style="border:1px solid #26344d;border-radius:9px;padding:1.25rem 1.4rem;margin:1rem 0;">';
    html += '<div style="font-size:1.5rem;font-weight:bold;">' +
      escapeHtml(number) +
      ' <span style="font-size:1rem;font-weight:normal;opacity:.65;margin-left:.5rem;">' +
      language + '</span></div>';

    if (lemma || english || searchHint) {
      html += '<div style="font-size:2rem;margin:.75rem 0;">';
      if (lemma) html += escapeHtml(lemma);
      if (english) {
        html += ' <span style="font-size:1.25rem;opacity:.75;">— ' + escapeHtml(english) + '</span>';
      } else if (searchHint) {
        html += ' <span style="font-size:1.25rem;opacity:.55;">— [' + escapeHtml(searchHint) + ']</span>';
      }
      html += '</div>';
    }

    if (entry.xlit) html += '<p><strong>Transliteration:</strong> ' + escapeHtml(entry.xlit) + '</p>';
    if (entry.pronounce) html += '<p><strong>Pronunciation:</strong> ' + escapeHtml(entry.pronounce) + '</p>';
    if (description) html += '<p style="line-height:1.65;">' + highlightSearch(description, query) + '</p>';
    html += '</div>';
    return html;
  }

  function searchEntries() {
    var rawQuery = searchBox.value.trim();

    if (!rawQuery) {
      resultsBox.innerHTML = '';
      statusBox.innerHTML = '<p><strong>' + entries.length.toLocaleString() +
        '</strong> entries loaded — 8,674 Hebrew and 5,624 Greek.</p>';
      return;
    }

    var query = rawQuery.toLowerCase();
    var normalizedNumber = rawQuery.toUpperCase();

    if (/^[GH]0*\d+$/.test(normalizedNumber)) {
      normalizedNumber = normalizedNumber.charAt(0) + parseInt(normalizedNumber.substring(1), 10);
    }

    var matches = [];

    for (var i = 0; i < entries.length; i++) {
      var entry = entries[i];
      var number = String(entry.number || '');
      var lemma = String(entry.lemma || '').toLowerCase();
      var english = String(entry.english || '').toLowerCase();
      var xlit = String(entry.xlit || '').toLowerCase();
      var pronounce = String(entry.pronounce || '').toLowerCase();
      var description = String(entry.description || '').toLowerCase();

      if (
        number.toUpperCase() === normalizedNumber ||
        number.toLowerCase().indexOf(query) !== -1 ||
        lemma.indexOf(query) !== -1 ||
        english.indexOf(query) !== -1 ||
        xlit.indexOf(query) !== -1 ||
        pronounce.indexOf(query) !== -1 ||
        description.indexOf(query) !== -1
      ) matches.push(entry);

      if (matches.length === 50) break;
    }

    if (!matches.length) {
      statusBox.innerHTML = '<p>No matching Strong\'s entries for <strong>' +
        escapeHtml(rawQuery) + '</strong>.</p>';
      resultsBox.innerHTML = '';
      return;
    }

    statusBox.innerHTML = '<p><strong>' + matches.length +
      (matches.length === 50 ? '+' : '') + '</strong> matching entries.</p>';

    var output = '';
    for (var j = 0; j < matches.length; j++) output += renderEntry(matches[j], rawQuery);
    resultsBox.innerHTML = output;
  }

  searchBox.addEventListener('input', searchEntries);

  var xhr = new XMLHttpRequest();
  xhr.open('GET', '/bkv/meta/strongs/strongs.json', true);

  xhr.onload = function () {
    if (xhr.status < 200 || xhr.status >= 300) {
      statusBox.innerHTML = '<p><strong>Could not load Strong\'s data.</strong> HTTP ' + xhr.status + '</p>';
      return;
    }

    var data;
    try {
      data = JSON.parse(xhr.responseText);
    } catch (error) {
      statusBox.innerHTML = '<p><strong>The Strong\'s file loaded, but the JSON could not be parsed.</strong><br>' +
        escapeHtml(error.message) + '</p>';
      return;
    }

    if (!Array.isArray(data)) {
      statusBox.innerHTML = '<p><strong>The Strong\'s file loaded, but its structure was not recognized.</strong></p>';
      return;
    }

    entries = data;
    searchBox.disabled = false;
    searchBox.placeholder = 'Try sword, love, Abraham, agape, H2719, G26...';
    statusBox.innerHTML = '<p><strong>' + entries.length.toLocaleString() +
      '</strong> entries loaded — 8,674 Hebrew and 5,624 Greek.</p>';
  };

  xhr.onerror = function () {
    statusBox.innerHTML = '<p><strong>The Strong\'s file request failed.</strong></p>';
  };

  xhr.send();
})();
</script>

---

<h2 id="potts-search-section">Potts — Swedenborg Concordance</h2>

Search John Faulkner Potts's <em>Swedenborg Concordance</em> by subject, alternate headword, Latin term, or Swedenborg work.

<div id="potts-app"></div>

<script>
(function () {
  var app = document.getElementById('potts-app');

  var searchBox = document.createElement('input');
  searchBox.type = 'search';
  searchBox.placeholder = 'Loading Potts Concordance...';
  searchBox.autocomplete = 'off';
  searchBox.disabled = true;
  searchBox.style.width = '100%';
  searchBox.style.maxWidth = '700px';
  searchBox.style.padding = '14px 16px';
  searchBox.style.fontSize = '18px';
  searchBox.style.margin = '20px 0 8px';
  searchBox.style.boxSizing = 'border-box';

  var statusBox = document.createElement('div');
  var resultsBox = document.createElement('div');

  statusBox.innerHTML = '<p>Loading Potts Concordance...</p>';

  app.appendChild(searchBox);
  app.appendChild(statusBox);
  app.appendChild(resultsBox);

  var entries = [];

  function escapeHtml(value) {
    return String(value == null ? '' : value)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  function asArray(value) {
    if (Array.isArray(value)) return value;
    if (value == null || value === '') return [];
    return [value];
  }

  function searchEntries() {
    var rawQuery = searchBox.value.trim();

    if (!rawQuery) {
      resultsBox.innerHTML = '';
      statusBox.innerHTML =
        '<p><strong>' + entries.length.toLocaleString() + '</strong> Potts articles available.</p>';
      return;
    }

    var q = rawQuery.toLowerCase();

    var matches = entries.filter(function (entry) {
      var searchable = []
        .concat(entry.term || '')
        .concat(asArray(entry.headwords))
        .concat(asArray(entry.latin))
        .concat(asArray(entry.works))
        .concat(asArray(entry.header_sentences))
        .join(' ')
        .toLowerCase();

      return searchable.indexOf(q) !== -1;
    }).slice(0, 50);

    if (!matches.length) {
      statusBox.innerHTML =
        '<p>No matching Potts entries for <strong>' + escapeHtml(rawQuery) + '</strong>.</p>';
      resultsBox.innerHTML = '';
      return;
    }

    statusBox.innerHTML =
      '<p><strong>' + matches.length + (matches.length === 50 ? '+' : '') +
      '</strong> matching Potts entries.</p>';

    resultsBox.innerHTML = matches.map(function (entry) {
      var term = entry.term || (entry.headwords && entry.headwords[0]) || 'Untitled entry';
      var latin = asArray(entry.latin);
      var works = asArray(entry.works);
      var headwords = asArray(entry.headwords).filter(function (h) {
        return h && h !== term;
      });

      var html =
        '<div style="border:1px solid #26344d;border-radius:9px;padding:1.1rem 1.25rem;margin:1rem 0;">' +
        '<div style="font-size:1.35rem;font-weight:bold;">' + escapeHtml(term) + '</div>';

      if (latin.length) {
        html += '<p style="margin:.45rem 0;"><em>' +
          latin.map(escapeHtml).join(' · ') + '</em></p>';
      }

      if (headwords.length) {
        html += '<p style="margin:.45rem 0;"><strong>Related:</strong> ' +
          headwords.map(escapeHtml).join(' · ') + '</p>';
      }

      if (works.length) {
        html += '<p style="margin:.45rem 0;opacity:.78;"><strong>Works:</strong> ' +
          works.map(escapeHtml).join(' · ') + '</p>';
      }

      // Only Obedience has a published Potts article page at this stage.
      if ((entry.slug || '').toLowerCase() === 'obedience') {
        html += '<p style="margin:.7rem 0 0;"><a href="{{ \'/meta/potts/obedience/\' | relative_url }}"><strong>Open entry →</strong></a></p>';
      } else {
        html += '<p style="margin:.7rem 0 0;opacity:.55;"><em>Full entry page coming next.</em></p>';
      }

      html += '</div>';
      return html;
    }).join('');
  }

  searchBox.addEventListener('input', searchEntries);

  fetch('{{ "/meta/potts/potts-index.json" | relative_url }}')
    .then(function (response) {
      if (!response.ok) throw new Error('HTTP ' + response.status);
      return response.json();
    })
    .then(function (data) {
      if (!Array.isArray(data)) {
        throw new Error('Potts index is not an array.');
      }

      entries = data;
      searchBox.disabled = false;
      searchBox.placeholder = 'Try obedience, Aaron, love, hear, Obedientia...';
      statusBox.innerHTML =
        '<p><strong>' + entries.length.toLocaleString() + '</strong> Potts articles available.</p>';
    })
    .catch(function (error) {
      console.error(error);
      statusBox.innerHTML =
        '<p><strong>The Potts Concordance could not be loaded.</strong></p>';
    });
})();
</script>

