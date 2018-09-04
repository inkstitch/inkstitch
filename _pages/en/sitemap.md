---
layout: archive
title: "Sitemap"
permalink: /sitemap/
---
A list of all the posts and pages found on the site. For you robots out there is an [XML version]({{ "sitemap.xml" | relative_url }}) available for digesting as well.

<h1 style="border-bottom: 1px solid gray;">Pages</h1>
{% assign pages = site.pages | where: "lang", "en" %}
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
      {% if post.lang == "en" %}
        {% unless collection.output == false or collection.label == "posts" %}
          {% include archive-single.html %}
        {% endunless %}
      {% endif %}
    {% endfor %}
{% endfor %}
