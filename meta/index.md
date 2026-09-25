---
title: "Metaphysical Bible Dictionary"
permalink: /meta/
---

# Metaphysical Bible Dictionary

Search Charles Fillmore's *Metaphysical Bible Dictionary*.

<input
  type="search"
  id="fillmore-search"
  placeholder="Search a name, place, or term..."
  autocomplete="off"
  style="width:100%;max-width:700px;padding:14px 16px;font-size:18px;margin:20px 0;"
>

<div id="fillmore-results"></div>

<script>
const search = document.getElementById('fillmore-search');
const results = document.getElementById('fillmore-results');
let entries = [];

fetch('{{ "/assets/data/fillmore-index.json" | relative_url }}')
  .then(response => response.json())
  .then(data => {
    entries = data;
    results.innerHTML = `<p>${entries.length.toLocaleString()} entries available.</p>`;
  });

search.addEventListener('input', function () {
  const q = this.value.trim().toLowerCase();

  if (!q) {
    results.innerHTML = `<p>${entries.length.toLocaleString()} entries available.</p>`;
    return;
  }

  const matches = entries
    .filter(entry => entry.term.toLowerCase().includes(q))
    .slice(0, 50);

  if (!matches.length) {
    results.innerHTML = '<p>No matching entries.</p>';
    return;
  }

  results.innerHTML = matches.map(entry =>
    `<p><a href="${entry.url}">${entry.term}</a></p>`
  ).join('');
});
</script>
