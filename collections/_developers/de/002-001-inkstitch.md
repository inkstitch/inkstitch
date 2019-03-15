---
title: "Developing Ink/Stitch"
permalink: /de/developers/inkstitch/
last_modified_at: 2019-03-15
toc: true
---
## Ink/Stitch Organisation
Der [Plugin-Code](https://github.com/inkstitch/inkstitch) als auch das [Pyembroidery Repository](https://github.com/inkstitch/pyembroidery) sind unter der [Ink/Stitch Organisation](https://github.com/inkstitch/) auf GitHub zusammengefasst. Außerdem gibt es dort noch andere nützliche Dinge, wie beispielsweise [Stickschriftarten](https://github.com/inkstitch/embroidery-fonts).

## Inkscape Plugin
Ink/Stitch ist ein [Inkscape](https://inkscape.org/) Plugin. Auf deren Webseite gibt es eine kurze Einführung darüber, [wie man ein Inkscape Plugin schreibt](https://inkscape.org/en/develop/extensions/).

## Ink/Stitch Programmier-Sprachen

Ink/Stitch und pyembroidery sind in [Python](https://www.python.org/) 2 geschrieben.

Ein Update auf Python 3 ist derzeit nicht möglich, da inkex.py, das Erweiterungen-Framework für Inkscape, nur in Python 2 existiert.

Der im Browser dargestellte PDF-Ausdruck benutzt die typischen Web-Skriptsprachen wie HTML5, CSS und Javascript (JQuery). Dabei kommt außerdem das [Jinja Template Framework](http://jinja.pocoo.org/) zum Einsatz.

## Entwickler Dokumentation
* [Manualle Installation](/de/developers/inkstitch/manual-setup/)
* [Python Module](/de/developers/inkstitch/python-modules/)
