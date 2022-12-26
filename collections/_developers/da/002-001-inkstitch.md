---
title: "Developing Ink/Stitch"
permalink: /da/developers/inkstitch/
last_modified_at: 2022-10-08
toc: true
---
## Ink/Stitch Organization
The [plugin code](https://github.com/inkstitch/inkstitch) as well as the [pyembroidery repository](https://github.com/inkstitch/pyembroidery) can be found within the [Ink/Stitch organization](https://github.com/inkstitch/) on GitHub.

## Inkscape Plugin
Ink/Stitch is an [Inkscape](https://inkscape.org/) plugin. Have a look at the [inkex documentation](https://inkscape.gitlab.io/extensions/documentation/) on their website to learn more about how to write Inkscape plugins.

## Ink/Stitch Languages

Ink/Stitch and pyembroidery are written in [Python](https://www.python.org/) 3.8. Python 3.8 is the last python version which is supported by Windows 7.

Print PDF and the Simulator use Electron with Vue. The print preview uses the [Jinja Template Framework](http://jinja.pocoo.org/), which may be converted to be using vue.js in future versions.

## Developers Documentation
* [Manual Setup](/developers/inkstitch/manual-setup/)
* [Python Modules](/developers/inkstitch/python-modules/)
