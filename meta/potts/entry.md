---
title: "Potts — Swedenborg Concordance"
permalink: /meta/potts/entry/
---

# Potts — Swedenborg Concordance

<div id="potts-entry">
  <p>Loading Potts entry...</p>
</div>

<p><a href="{{ '/meta/#potts-search-section' | relative_url }}">← Back to Potts search</a></p>

<script>
(function () {
  var app = document.getElementById('potts-entry');
  var params = new URLSearchParams(window.location.search);
  var slug = params.get('entry');

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

  function referenceLabel(ref) {
    if (!ref) return '';
    var label = ref.work || '';
    if (ref.section) label += (label ? ' ' : '') + ref.section;
    if (ref.subsection) label += ':' + ref.subsection;
    return label;
  }

  function renderEntry(entry) {
    document.title = (entry.term || 'Potts Entry') + ' — The Bible Key Vision';

    var term = entry.term || 'Potts Entry';
    var latin = asArray(entry.latin);
    var headwords = asArray(entry.headwords).filter(function (h) {
      return h && h !== term;
    });
    var sentences = asArray(entry.header_sentences);
    var contexts = asArray(entry.contexts);

    var html = '<h1>' + escapeHtml(term) + '</h1>';

    if (latin.length) {
      html += '<p><strong>Latin:</strong> <em>' +
        latin.map(escapeHtml).join(' · ') + '</em></p>';
    }

    if (headwords.length) {
      html += '<p><strong>Related terms:</strong> ' +
        headwords.map(escapeHtml).join(' · ') + '</p>';
    }

    if (sentences.length) {
      html += sentences.map(function (s) {
        return '<p>' + escapeHtml(s) + '</p>';
      }).join('');
    }

    if (entry.redirect_xref && !contexts.length) {
      html += '<p><em>This Potts record is a cross-reference entry.</em></p>';
    }

    if (!contexts.length) {
      html += '<p>No contextual quotations are stored for this entry.</p>';
      app.innerHTML = html;
      return;
    }

    var groups = {};
    var order = [];

    contexts.forEach(function (ctx) {
      var work = (ctx.reference && ctx.reference.work) || 'Other';
      if (!groups[work]) {
        groups[work] = [];
        order.push(work);
      }
      groups[work].push(ctx);
    });

    order.forEach(function (work) {
      html += '<h2>' + escapeHtml(work) + '</h2>';

      groups[work].forEach(function (ctx) {
        var ref = referenceLabel(ctx.reference);
        html += '<div style="margin:1rem 0 1.35rem;padding-bottom:1rem;border-bottom:1px solid #26344d;">';

        if (ref) {
          html += '<p style="margin-bottom:.35rem;"><strong>' + escapeHtml(ref) + '</strong></p>';
        }

        if (ctx.text) {
          html += '<p style="line-height:1.65;margin-top:.35rem;">' +
            escapeHtml(ctx.text) + '</p>';
        }

        if (ctx.comment) {
          html += '<p><em>' + escapeHtml(ctx.comment) + '</em></p>';
        }

        if (ctx.footnote) {
          html += '<p style="font-size:.9em;opacity:.75;">' +
            escapeHtml(ctx.footnote) + '</p>';
        }

        html += '</div>';
      });
    });

    app.innerHTML = html;
  }

  if (!slug || !/^[a-z0-9-]+$/.test(slug)) {
    app.innerHTML = '<h1>Potts Entry</h1><p>No valid entry was specified.</p>';
    return;
  }

  fetch('{{ "/meta/potts/data/" | relative_url }}' + encodeURIComponent(slug) + '.json')
    .then(function (response) {
      if (!response.ok) throw new Error('HTTP ' + response.status);
      return response.json();
    })
    .then(renderEntry)
    .catch(function (error) {
      console.error(error);
      app.innerHTML =
        '<h1>Potts Entry</h1><p><strong>This entry could not be loaded.</strong></p>';
    });
})();
</script>
