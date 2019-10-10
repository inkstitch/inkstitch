---
title: "Install Ink/Stitch"
permalink: /fr/docs/install/
excerpt: "How to quickly install Ink/Stitch."
last_modified_at: 2019-08-11
toc: true
---

**Info:** We also provide beginner tutorial videos on our <i class="fab fa-youtube"></i> [YouTube channel](https://www.youtube.com/channel/UCJCDCFuT_xQoI55e10HRiRw).<br />
For the installation process watch the video for
<i class="fab fa-linux"></i>&nbsp;[Linux](https://www.youtube.com/watch?v=Dkb5UvsZUNg&list=PLvlbfDmZyXG1ORmeqHdp4aP7J71e7icJP&index=2),
<i class="fab fa-apple"></i>&nbsp;[macOS](https://www.youtube.com/watch?v=gmOVLNh9cu8&list=PLvlbfDmZyXG1ORmeqHdp4aP7J71e7icJP&index=3) or
<i class="fab fa-windows"></i>&nbsp;[Windows](https://www.youtube.com/watch?v=U5htzWZSjA8&list=PLvlbfDmZyXG1ORmeqHdp4aP7J71e7icJP&index=4).
{: .notice--info }

## Requirements

* [Inkscape](https://inkscape.org/) Version 0.92.2 or higher
* Modern Browser for the Print Preview

That's it!  All python libraries and external dependencies are bundled (using the excellent [pyinstaller](http://www.pyinstaller.org)), so you shouldn't need to set anything else up.

**Info:** Inkscape Version 0.92 or greater, has a really key feature: the *Objects panel*.<br>
This gives you a heirarchical list of objects in your SVG file, listed in their stacking order. This is really important because the stacking order dictates the order that the shapes will be sewn in.<br><br>
Versions 0.92.2 and higher let you [bind a key](/docs/customize/#shortcut-keys) to new commands, “stack up” and “stack down”, which you can assign to pageup and pagedown. These let you arbitrarily reorder objects in the SVG file, which lets you directly manipulate which order they stitch in. It works way better than the default “raise” and “lower” commands.
{: .notice--info }

## Quick Setup

### 1. Download
Download the release archive for your platform from [latest release](https://github.com/inkstitch/inkstitch/releases/latest).

OS|File name|32&#8209;bit|64&#8209;bit
---|---|---|---
Linux|inkstitch-[VERSION]-Linux-x86_64-[LOCALE].tar.gz|☒|☑
Windows|inkstitch-[VERSION]-win32-[LOCALE].zip|☑|☑
macOS|inkstitch-[VERSION]-osx-x86_64-[LOCALE].tar.gz|☒|☑

The `LOCALE` selected affects the menus shown inside Inkscape. Ink/Stitch dialogs are in the lanugage of your OS (if that language is supported).

**Info:** Ink/Stitch for macOS currently works only with Sierra (10.12) and higher.
{: .notice--warning }

### 2. Install
 * In Inkscape, go to `Edit > Preferences > System` and check where your `User Extensions` folder is.
 * Decompress the Ink/Stitch archive **directly** into this folder.<br />
   In this folder the file structure should look similiar to this (just a lot more files):
   ![File Structure](/assets/images/docs/en/file_structure.png)
 * Restart Inkscape.
 * You will then find Ink/Stitch under `Extensions > Ink/Stitch`.

#### Linux and macOS:

 ```
 $ cd ~/.config/inkscape/extensions
 $ tar zxf ~/Downloads/inkstitch-v1.0.0-Linux-x86_64.tar.gz
 ```

#### Windows

 * Unhide the AppData directory (go to `C:\Users\%USERNAME%\`, e.g. `C:\Users\Janet`)
 * Unzip in `C:\Users\%USERNAME%\AppData\Roaming\inkscape\extensions`

## Upgrade

 * You may have to delete the old extension files first:<br />
   Go to the extension directory and remove each inkstitch* file and folder.
 * Then, proceed as above.

**Tip:** Subscribe to a news feed channel to keep track on Ink/Stitch Updates:<br />
 <i class="fas fa-fw fa-rss-square" aria-hidden="true" style="color: #ffb400;"></i> [GitHub Feed on new Releases](https://github.com/inkstitch/inkstitch/releases.atom)<br>
 <i class="fas fa-fw fa-rss-square" aria-hidden="true" style="color: #ffb400;"></i> [Ink/Stitch News](/feed.xml)<br />
{: .notice--info }

<p class="notice--info" style="margin-top: -3.5em !important;">Or watch the project on GitHub:<br /><iframe style="display: inline-block;" src="https://ghbtns.com/github-btn.html?user=inkstitch&repo=inkstitch&type=watch&count=true&v=2" frameborder="0" scrolling="0" width="170px" height="20px"></iframe></p>

## Manual Setup

It is possible to install Ink/Stitch manually. It is not recommended though - unless you want to help developing the extension.
In this case, please have a look at the [developer documentation](/developers/inkstitch/manual-setup/) section.

