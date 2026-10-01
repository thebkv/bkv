---
title: "Biblical Symbolics"
permalink: /symbolics/
---

# Biblical Symbolics

Biblical symbols develop their meaning through the way they function across Scripture. This library follows those recurring uses and records the symbolic patterns that emerge.

<div style="margin-top:2rem;">

{% assign symbolic_pages = site.pages | where_exp: "p", "p.path contains 'symbolics/'" | sort: "title" %}

{% for p in symbolic_pages %}
  {% unless p.name == 'index.md' %}
  <a href="{{ p.url | relative_url }}" style="display:block;border:1px solid #26344d;border-radius:9px;padding:1rem 1.2rem;margin-bottom:.75rem;text-decoration:none;">
    <strong>{{ p.title }}</strong>
  </a>
  {% endunless %}
{% endfor %}

</div>

---

[← Reference Library]({{ '/meta/' | relative_url }})
