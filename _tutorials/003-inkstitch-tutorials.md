---
title: "Ink/Stitch Tutorials"
permalink: /tutorials/inkstitch-tutorials/
excerpt: ""
last_modified_at: 2018-05-14
read_time: false
classes: wide
---
{% comment %}This is the list of keys you can set to categorize tutorials, use slugified version in tutorial file: f.e. Tutorial Type would become tutorial-type{% endcomment %}
{% assign tutorial_cats = 'Tutorial Type*Stitch Type*Techniques*Field Of Use*User Level' | split: '*' %}

{% include display_tutorials tutorial_cats=tutorial_cats %}
