---
title: "Ink/Stitch Tutorials"
permalink: /de/tutorials/
read_time: false
classes: wide
---
{% comment %}This is the list of keys you can set to categorize tutorials, use slugified version in tutorial file: f.e. Tutorial Type would become tutorial-type{% endcomment %}
{% assign tutorial_cats = 'Tutorial Typ*Stichart*Techniken*Schwierigkeitsgrad' | split: '*' %}

{% include tutorials/display_tutorials tutorial_cats=tutorial_cats %}
