---
title: "Reference Library"
permalink: /meta/
---

# Reference Library

Patterns, names, meanings, and tools for following Scripture across the whole Bible.

---

## Fractal Patterns

Some movements appear again and again in Scripture. The people and places change, but the movement remains.

These pages follow those patterns through the Bible and ask where the same movement happens in the disciple.

### [The Younger Supplants the Elder]({{ '/fractals/younger-supplants-elder/' | relative_url }})

**Natural first. Spiritual afterward.**

Again and again, the one who comes first is not the one who finally carries the inheritance: Cain and Abel, Ishmael and Isaac, Esau and Jacob, Saul and David, Adam and Christ.

[Explore all fractal patterns →]({{ '/fractals/' | relative_url }})

---

## Metaphysical Bible Dictionary

Search Charles Fillmore's *Metaphysical Bible Dictionary*.

<input type="search" id="fillmore-search" placeholder="Search a name, place, or term..." autocomplete="off" style="width:100%;max-width:700px;padding:14px 16px;font-size:18px;margin:20px 0;">

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
    `<p><a href="/bkv${entry.url}">${entry.term}</a></p>`
  ).join('');
});
</script>
