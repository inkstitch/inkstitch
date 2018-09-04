---
layout: archive
title: "Sitemap"
permalink: /de/sitemap/
---
Dies ist eine Liste aller Seiten, die du auf Ink/Stitch finden kannst. Für euch Roboter da draußen gibt es auch eine [XML version]({{ "sitemap.xml" | relative_url }}).

<h1 style="border-bottom: 1px solid gray;">Seiten</h1>
{% assign pages = site.pages | where: "lang", "de" %}
{% for post in pages  %}
  {% include archive-single.html %}
{% endfor %}

{% assign written_label = 'None' %}

{% for collection in site.collections  %}
    {% unless collection.output == false or collection.label == "posts" %}
{{  collection.blubb }}
      {% capture label %}{{ collection.label }}{% endcapture %}
      {% if label != written_label %}
<h1 style="border-bottom: 1px solid gray; margin-top: 1.5em;">{{ label }}</h1>
      {% assign written_label = label %}
      {% endif %}
    {% endunless %}
    {% for post in collection.docs %}
      {% if post.lang == "de" %}
        {% unless collection.output == false or collection.label == "posts" %}
          {% include archive-single.html %}
        {% endunless %}
      {% endif %}
    {% endfor %}
{% endfor %}
