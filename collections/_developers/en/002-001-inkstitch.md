---
title: "Developing Ink/Stitch"
permalink: /developers/inkstitch/
last_modified_at: 2021-12-27
toc: true
---
## Ink/Stitch Organization
The [plugin code](https://github.com/inkstitch/inkstitch) as well as the [pyembroidery repository](https://github.com/inkstitch/pyembroidery) can be found within the [Ink/Stitch organization](https://github.com/inkstitch/) on github. Additionally, you will find some other useful things like [embroidery fonts](https://github.com/inkstitch/embroidery-fonts).

## Inkscape Plugin
Ink/Stitch is an [Inkscape](https://inkscape.org/) plugin. See their website to read a short introduction about [how to write Inkscape plugins](https://inkscape.org/en/develop/extensions/).

## Ink/Stitch Languages

Ink/Stitch and pyembroidery are written in [Python](https://www.python.org/) 2.<br />We cannot use Python 3 because inkex.py, the extension framework for Inkscape, is in Python 2 only.

Print PDF uses Electron. Which will lead the whole GUI to be displayed with the help of web languages such as HTML5, CSS and Javascript. The print preview uses the [Jinja Template Framework](http://jinja.pocoo.org/), which might be converted to be using vue.js in future versions.

## Developers Documentation
* [Manual Setup](/developers/inkstitch/manual-setup/)
* [Python Modules](/developers/inkstitch/python-modules/)
