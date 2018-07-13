---
title: "Install Ink/Stitch"
permalink: /docs/install/
excerpt: "How to quickly install Ink/Stitch."
last_modified_at: 2018-06-04
toc: true
---

## Requirements

* [Inkscape](https://inkscape.org/) Version 0.92.2 or higher

That's it!  All python libraries and external dependencies are bundled (using the excellent [pyinstaller](http://www.pyinstaller.org)), so you shouldn't need to set anything else up.

**Info:** Inkscape Version 0.92 or greater, has a really key feature: the *Objects panel*.<br>
This gives you a heirarchical list of objects in your SVG file, listed in their stacking order. This is really important because the stacking order dictates the order that the shapes will be sewn in.<br><br>
Versions 0.92.2 and higher let you [bind a key](/docs/customize/#shortcut-keys) to new commands, “stack up” and “stack down”, which you can assign to pageup and pagedown. These let you arbitrarily reorder objects in the SVG file, which lets you directly manipulate which order they stitch in. It works way better than the default “raise” and “lower” commands.
{: .notice--info }

## Quick Setup

### 1. Download
Download the right release archive for your platform from the [latest release](https://github.com/inkstitch/inkstitch/releases/latest).

OS|File name|32&#8209;bit|64&#8209;bit
---|---|---|---
Linux|`inkstitch-[VERSION]-Linux-x86_64.tar.gz`|☒|☑
Windows|`inkstitch-[VERSION]-win32.zip`|☑|☑
macOS|Sorry, there is no macOS-Version yet. If you are willing to [test](https://github.com/inkstitch/inkstitch/releases/tag/dev-build-lexelby-mac-build-mk2) or help building it, contact us through [GitHub](https://github.com/inkstitch/inkstitch/pull/181).|☒|☒

### 2. Install
 * In Inkscape, go to `Edit > Preferences > System` and check where your `User Extensions` folder is.
 * Decompress the the Ink/Stitch archive directly into this folder and restart Inkscape.
 * You will then find Ink/Stitch under `Extensions > Embroidery`.

#### For example on Linux:

```
$ cd ~/.config/inkscape/extensions
$ tar zxf ~/Downloads/inkstitch-v1.0.0-Linux-x86_64.tar.gz
```

#### For example on Windows

* Unhide the AppData directory (go to `C:\Users\%USERNAME%\`, e.g. `C:\Users\Janet`
* Unzip in `C:\Users\%USERNAME%\AppData\Roaming\inkscape\extensions`

## Upgrade

 * You may have to delete the old extension files first:<br>
   Go to the extension directory and remove each inkstitch* file.
 * Then, proceed as above.

**Tipp:** Subscribe to a news feed channel to keep track on Ink/Stitch Updates:<br>
 <i class="fas fa-fw fa-rss-square" aria-hidden="true" style="color: #ffb400;"></i> [GitHub Feed on new Releases](https://github.com/inkstitch/inkstitch/releases.atom)<br>
 <i class="fas fa-fw fa-rss-square" aria-hidden="true" style="color: #ffb400;"></i> [Ink/Stitch News](/feed.xml)<br>
{: .notice--info }

<p class="notice--info" style="margin-top: -3.5em !important;">Or watch the project on GitHub:<br><iframe style="display: inline-block;" src="https://ghbtns.com/github-btn.html?user=lexelby&repo=inkstitch&type=watch&count=true&v=2" frameborder="0" scrolling="0" width="170px" height="20px"></iframe></p>

## Manual Setup

### Python Dependencies
A few python modules are needed.  In some cases this extension uses features that aren't available in the versions of the modules pre-packaged in distributions, so I recommend installing them directly with pip:

```
pip install -r requirements.txt
```

### Extension Installation
1. Clone the extension source: `git clone https://github.com/inkstitch/inkstitch`
2. Install it as directed [here](https://inkscape.org/en/gallery/%3Dextension/)

**Tipp:** Symbolically link into your git clone, which allows you to hack on the code. Changes to the Python code take effect the next time the extension is run.  Changes to the extension description files (`*.inx`) take effect the next time Inkscape is restarted.
{: .notice--info }
