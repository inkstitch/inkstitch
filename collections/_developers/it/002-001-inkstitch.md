---
title: "Sviluppo di Ink/Stitch"
permalink: /developers/inkstitch/
last_modified_at: 2022-10-09
toc: true
---
## Organizzazione Ink/Stitch

Il [codice del plugin](https://github.com/inkstitch/inkstitch) così come il [repository di pyembroidery](https://github.com/inkstitch/pyembroidery) possono essere trovati all'interno dell'organizzazione [Ink/Stitch](https://github.com/inkstitch/) su GitHub.

## Plugin per Inkscape

Ink/Stitch è un [plugin per Inkscape](https://inkscape.org/). Consultare la [documentazione di Inkex](https://inkscape.gitlab.io/extensions/documentation/) sul loro sito web per saperne di più su come scrivere plugin per Inkscape.

## Lingue di Ink/Stitch

Ink/Stitch e pyembroidery sono scritti in [Python](https://www.python.org/) 3.8. Python 3.8 è l'ultima versione di Python supportata da Windows 7.

La funzione di stampa in PDF e il simulatore utilizzano Electron con Vue. L'anteprima di stampa utilizza il [Jinja Template Framework](http://jinja.pocoo.org/), che potrebbe essere convertito per utilizzare vue.js in versioni future.

## Documentazione per sviluppatori

* [Configurazione manuale](/developers/inkstitch/manual-setup/)
* [Moduli Python](/developers/inkstitch/python-modules/)