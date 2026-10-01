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
      <a href="{{ '/meta/strongs/' | relative_url }}"><strong>Strong's Hebrew & Greek →</strong></a>
    </p>

    <p style="margin-bottom:0;">
      <a href="{{ '/meta/potts/obedience/' | relative_url }}"><strong>Potts Concordance — Obedience →</strong></a>
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

<input
  type="search"
  id="fillmore-search"
  placeholder="Search a name, place, or term..."
  autocomplete="off"
  style="width:100%;max-width:700px;padding:14px 16px;font-size:18px;margin:20px 0 8px;"
>

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
