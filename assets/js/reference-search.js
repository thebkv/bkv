(() => {
  const form = document.getElementById('reference-search');
  const input = document.getElementById('reference-query');
  const results = document.getElementById('reference-results');
  const base = form.dataset.base;
  const limit = 10;

  function normalize(value) {
    return String(value ?? '').normalize('NFC').toLowerCase().trim().replace(/\s+/g, ' ');
  }

  function rank(entry, query, primaryFields, broaderFields) {
    const primary = primaryFields.flatMap(field => entry[field] ?? []).map(normalize);
    const broader = broaderFields.flatMap(field => entry[field] ?? []).map(normalize);
    const words = text => text.split(/[^\p{L}\p{M}\p{N}]+/u);
    const containsWords = text => (' ' + words(text).join(' ') + ' ').includes(' ' + query + ' ');

    if (primary[0] === query) return 0;
    if (primary.includes(query)) return 1;
    if (primary.some(containsWords)) return 2;
    if (primary.some(text => words(text).some(word => word.startsWith(query)))) return 3;
    if (broader.some(text => text === query || containsWords(text))) return 4;
    return Infinity;
  }

  const sources = [
    {
      title: 'Fillmore',
      url: form.dataset.fillmore,
      primary: ['term'],
      broader: [],
      label: entry => entry.term,
      link: entry => base + entry.url
    },
    {
      title: 'Potts',
      url: form.dataset.potts,
      primary: ['term', 'headwords', 'latin'],
      broader: ['works', 'header_sentences'],
      label: entry => entry.term,
      link: entry => form.dataset.pottsEntry + '?entry=' + encodeURIComponent(entry.slug),
      note: entry => entry.latin?.join(' · ')
    },
    {
      title: 'Strong’s',
      url: form.dataset.strongs,
      primary: ['number', 'lemma', 'xlit', 'english'],
      broader: ['description'],
      label: entry => [entry.number, entry.lemma, entry.english].filter(Boolean).join(' · '),
      note: entry => entry.description
    }
  ];

  function load(source) {
    source.request ??= fetch(source.url)
      .then(response => {
        if (!response.ok) throw new Error('HTTP ' + response.status);
        return response.json();
      })
      .then(entries => {
        if (!Array.isArray(entries)) throw new Error('Expected an array of entries');
        return entries;
      })
      .catch(error => {
        delete source.request;
        throw error;
      });
    return source.request;
  }

  function element(tag, text) {
    const node = document.createElement(tag);
    node.textContent = text;
    return node;
  }

  function renderResult(source, entry) {
    const item = document.createElement('li');
    const label = element(source.link ? 'a' : 'strong', source.label(entry));
    if (source.link) label.href = source.link(entry);
    item.append(label);
    const note = source.note?.(entry);
    if (note) item.append(element('p', note));
    return item;
  }

  async function searchSource(source, query, output) {
    let entries;
    try {
      entries = await load(source);
    } catch {
      output.textContent = 'Could not load this source. Search again to retry.';
      return;
    }

    const matches = entries
      .map(entry => ({ entry, rank: rank(entry, query, source.primary, source.broader) }))
      .filter(match => Number.isFinite(match.rank))
      .sort((a, b) => a.rank - b.rank);

    if (!matches.length) {
      output.textContent = 'No matches.';
      return;
    }

    const count = element('p', matches.length + (matches.length === 1 ? ' match' : ' matches'));
    const list = document.createElement('ul');
    const more = element('button', 'Show more');
    more.type = 'button';
    let shown = 0;

    function showMore() {
      matches.slice(shown, shown + limit).forEach(({ entry }) => list.append(renderResult(source, entry)));
      shown = list.children.length;
      more.hidden = shown >= matches.length;
    }

    more.addEventListener('click', showMore);
    showMore();
    output.replaceChildren(count, list, more);
  }

  form.addEventListener('submit', event => {
    event.preventDefault();
    const query = normalize(input.value);
    results.replaceChildren();
    if (!query) {
      input.focus();
      return;
    }

    sources.forEach(source => {
      const section = document.createElement('section');
      const heading = element('h3', source.title);
      const output = element('div', 'Loading…');
      output.setAttribute('aria-live', 'polite');
      section.append(heading, output);
      results.append(section);
      searchSource(source, query, output);
    });
  });
})();
