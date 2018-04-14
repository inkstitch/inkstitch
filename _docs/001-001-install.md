---
title: "Install Ink/Stitch"
permalink: /docs/install/
excerpt: "How to quickly install Ink/Stitch."
last_modified_at: 2018-04-14
toc: true
---

## Inkscape
First, install Inkscape if you don’t have it. I highly recommend version 0.92 or greater, which has a really key feature: the Objects panel. This gives you a heirarchical list of objects in your SVG file, listed in their stacking order. This is really important because the stacking order dictates the order that the shapes will be sewn in.

Versions 0.92.2 and higher let you bind a key to new commands, “stack up” and “stack down”, which I assign to pageup and pagedown. These let you arbitrarily reorder objects in the SVG file, which lets you directly manipulate which order they stitch in. It works way better than the default “raise” and “lower” commands.

## Quick Setup On Ubuntu and Windows
First, download the right release archive for your platform from the [latest release](https://github.com/lexelby/inkstitch/releases/latest).

* **Linux**: `inkstitch-[VERSION]-Linux-x86_64.tar.gz`
  * Currently supports most 64-bit Linux systems from the last couple of years.
  * 32-bit support coming soon.
* **Windows**: `inkstitch-[VERSION]-win32.zip`
  * Supports 32-bit and 64-bit Windows

In Inkscape, go to Preferences and look under System.  Next to "User Extensions" is a folder.  Decompress the archive you downloaded directly into this folder.

For example, on Linux:

```
$ cd ~/.config/inkscape/extensions
$ tar zxf ~/Downloads/inkstitch-v1.0.0-Linux-x86_64.tar.gz
```

That's it!  All python libraries and external dependencies are bundled (using the excellent [pyinstaller](http://www.pyinstaller.org)), so you shouldn't need to set anything else up.  Just restart Inkscape and the extension should be ready to go.

## Manual Setup

### Python Dependencies
A few python modules are needed.  In some cases this extension uses features that aren't available in the versions of the modules pre-packaged in distributions, so I recommend installing them directly with pip:

```
pip install -r requirements.txt
```

### Extension installation
1. Clone the extension source: `git clone https://github.com/lexelby/inkstitch`
2. Install it as directed [here](https://inkscape.org/en/gallery/%3Dextension/)

I prefer to symbolically link into my git clone, which allows me to hack on the code.  Changes to the Python code take effect the next time the extension is run.  Changes to the extension description files (`*.inx`) take effect the next time Inkscape is restarted

## Upgrade

Simply replace the files in the extension folder with the newer version.
