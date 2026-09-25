---
title: "Reference Library"
permalink: /meta/
---

# Reference Library

Use these tools to follow names, places, structures, and recurring patterns across Scripture.

<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:1rem;margin:1.5rem 0 2.5rem;">

  <div style="border:1px solid #26344d;border-radius:9px;padding:1.2rem;">
    <h2 style="margin-top:0;">Names & Meanings</h2>
    <p>Look up biblical names, places, words, and symbols.</p>
    <p><strong>Bible Dictionary</strong> · Strong's Roots <em>(coming later)</em></p>
  </div>

  <div style="border:1px solid #26344d;border-radius:9px;padding:1.2rem;">
    <h2 style="margin-top:0;">The Biblical World</h2>
    <p>See how places and structures function in Scripture.</p>
    <p>Tabernacle · Temple · Egypt to Canaan · Jerusalem · Wilderness</p>
  </div>

  <a href="{{ '/fractals/' | relative_url }}" style="display:block;border:1px solid #26344d;border-radius:9px;padding:1.2rem;text-decoration:none;color:inherit;">
    <h2 style="margin-top:0;">Fractal Patterns</h2>
    <p>Follow movements that repeat throughout Scripture and in the disciple.</p>
    <p>Death and Resurrection · Younger Supplants the Elder · Exodus · Two Kings · Seed · Return</p>
  </a>

  <div style="border:1px solid #26344d;border-radius:9px;padding:1.2rem;">
    <h2 style="margin-top:0;">How to Read</h2>
    <p>Simple principles for recognizing the interior meaning without losing the actual text.</p>
    <p>Scripture interprets Scripture · Function before symbolism · The Savior Test · Selected insights from Fillmore, Swedenborg, Lamsa, and Nicoll</p>
  </div>

</div>

---

## Bible Dictionary

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
    `<p><a href="{{ site.baseurl }}${entry.url}">${entry.term}</a></p>`
  ).join('');
});
</script>
