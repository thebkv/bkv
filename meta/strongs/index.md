---
title: "Strong's Concordance"
permalink: /meta/strongs/
---

# Strong's Concordance

Look up the Hebrew and Greek words indexed in *Strong's Exhaustive Concordance*.

Search by **Strong's number, English meaning, transliteration, original Hebrew or Greek,** or a word in the definition.

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

  function renderEntry(entry) {
    var number = String(entry.number || '');
    var language = number.charAt(0) === 'H' ? 'Hebrew' : 'Greek';

    var html = '';

    html += '<div style="border:1px solid #26344d;border-radius:9px;padding:1.25rem 1.4rem;margin:1rem 0;">';

    html += '<div style="font-size:1.5rem;font-weight:bold;">' +
      escapeHtml(number) +
      ' <span style="font-size:1rem;font-weight:normal;opacity:.65;margin-left:.5rem;">' +
      language +
      '</span></div>';

    if (entry.lemma || entry.english) {
      html += '<div style="font-size:2rem;margin:.75rem 0;">';

      if (entry.lemma) {
        html += escapeHtml(entry.lemma);
      }

      if (entry.english) {
        html += ' <span style="font-size:1.25rem;opacity:.75;">— ' +
          escapeHtml(entry.english) +
          '</span>';
      }

      html += '</div>';
    }

    if (entry.xlit) {
      html += '<p><strong>Transliteration:</strong> ' +
        escapeHtml(entry.xlit) +
        '</p>';
    }

    if (entry.pronounce) {
      html += '<p><strong>Pronunciation:</strong> ' +
        escapeHtml(entry.pronounce) +
        '</p>';
    }

    if (entry.description) {
      html += '<p style="line-height:1.65;">' +
        escapeHtml(entry.description) +
        '</p>';
    }

    html += '</div>';

    return html;
  }

  function searchEntries() {
    var rawQuery = searchBox.value.trim();

    if (!rawQuery) {
      resultsBox.innerHTML = '';

      statusBox.innerHTML =
        '<p><strong>' +
        entries.length.toLocaleString() +
        '</strong> entries loaded — 8,674 Hebrew and 5,624 Greek.</p>';

      return;
    }

    var query = rawQuery.toLowerCase();
    var normalizedNumber = rawQuery.toUpperCase();

    if (/^[GH]0*\d+$/.test(normalizedNumber)) {
      normalizedNumber =
        normalizedNumber.charAt(0) +
        parseInt(normalizedNumber.substring(1), 10);
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
      ) {
        matches.push(entry);
      }

      if (matches.length === 50) {
        break;
      }
    }

    if (matches.length === 0) {
      statusBox.innerHTML =
        '<p>No matching Strong\'s entries for <strong>' +
        escapeHtml(rawQuery) +
        '</strong>.</p>';

      resultsBox.innerHTML = '';
      return;
    }

    statusBox.innerHTML =
      '<p><strong>' +
      matches.length +
      (matches.length === 50 ? '+' : '') +
      '</strong> matching entries.</p>';

    var output = '';

    for (var j = 0; j < matches.length; j++) {
      output += renderEntry(matches[j]);
    }

    resultsBox.innerHTML = output;
  }

  searchBox.addEventListener('input', searchEntries);

  var xhr = new XMLHttpRequest();

  xhr.open(
    'GET',
    '/bkv/meta/strongs/strongs.json',
    true
  );

  xhr.onload = function () {
    if (xhr.status < 200 || xhr.status >= 300) {
      statusBox.innerHTML =
        '<p><strong>Could not load Strong\'s data.</strong> HTTP ' +
        xhr.status +
        '</p>';

      return;
    }

    var data;

    try {
      data = JSON.parse(xhr.responseText);
    } catch (error) {
      statusBox.innerHTML =
        '<p><strong>The Strong\'s file loaded, but the JSON could not be parsed.</strong><br>' +
        escapeHtml(error.message) +
        '</p>';

      return;
    }

    if (!Array.isArray(data)) {
      statusBox.innerHTML =
        '<p><strong>The Strong\'s file loaded, but its structure was not recognized.</strong></p>';

      return;
    }

    entries = data;

    searchBox.disabled = false;

    searchBox.placeholder =
      'Try sword, love, Abraham, agape, H2719, G26...';

    statusBox.innerHTML =
      '<p><strong>' +
      entries.length.toLocaleString() +
      '</strong> entries loaded — 8,674 Hebrew and 5,624 Greek.</p>';
  };

  xhr.onerror = function () {
    statusBox.innerHTML =
      '<p><strong>The Strong\'s file request failed.</strong></p>';
  };

  xhr.send();
})();
</script>

---

[← Reference Library]({{ '/meta/' | relative_url }})
