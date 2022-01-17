---
title: "DévelopperInk/Stitch"
permalink: /fr/developers/inkstitch/
last_modified_at: 2022-01-16
toc: true
---
## Ink/Stitch Organization
Le [code du plugin](https://github.com/inkstitch/inkstitch) ainsi que le [dépôt de pyembroidery](https://github.com/inkstitch/pyembroidery) peuvent être trouvés dans  [l'organisation d'Ink/Stitch](https://github.com/inkstitch/) sur github.   De plus, vous y trouverez d'autres choses utiles telles que des [polices de broderie](https://github.com/inkstitch/embroidery-fonts).

## Plugin Inkscape 
Ink/Stitch est un plugin [Inkscape](https://inkscape.org/). Voir leur site web pour une courte introduction sur [la manière d'écrire des plugins Inkscape](https://inkscape.org/en/develop/extensions/).

## Les Langages d'Ink/Stitch 

Ink/Stitch et pyembroidery sont écrits en  [Python](https://www.python.org/) 2.<br /> Nous ne pouvons pas utiliser Python 3 car inkex.py, le framework d'extension for Inkscape, existe seulement en Python 2.

L'impression PDF utilise Electron. Ce qui conduira tout l'interface graphique a être affiché à l'aide des langages du web tels que  HTML5, CSS  et Javascript.
La prévisualisation utilise [Jinja Template Framework](http://jinja.pocoo.org/), qui pourrait être remplacé par l'utilisation de vue.js dans des futures versions.

## Documentation pour les développeurs
* [Installation manuelle](/developers/inkstitch/manual-setup/)
* [Modules Python](/developers/inkstitch/python-modules/)
