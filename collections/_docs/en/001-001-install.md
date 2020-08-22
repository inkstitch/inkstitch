---
title: "Install Ink/Stitch"
permalink: /docs/install/
excerpt: "How to quickly install Ink/Stitch."
last_modified_at: 2020-04-21
toc: true
---
## Video Guide

We also provide beginner tutorial videos on our <i class="fab fa-youtube"></i> [YouTube channel](https://www.youtube.com/channel/UCJCDCFuT_xQoI55e10HRiRw).

For the installation process watch the video for your operating system
* <i class="fab fa-linux"></i> [Linux](https://www.youtube.com/watch?v=Dkb5UvsZUNg&list=PLvlbfDmZyXG1ORmeqHdp4aP7J71e7icJP&index=2)
* <i class="fab fa-apple"></i> [macOS](https://www.youtube.com/watch?v=gmOVLNh9cu8&list=PLvlbfDmZyXG1ORmeqHdp4aP7J71e7icJP&index=3)
* <i class="fab fa-windows"></i> [Windows](https://www.youtube.com/watch?v=U5htzWZSjA8&list=PLvlbfDmZyXG1ORmeqHdp4aP7J71e7icJP&index=4)

## Requirements

* [Inkscape](https://inkscape.org/) Version 0.92.2 or higher (including [Inkscape](https://inkscape.org/release/inkscape-1.0/?latest=1) Version 1.0 RC)

That's it!  All python libraries and external dependencies are bundled (using the excellent [pyinstaller](http://www.pyinstaller.org)), so you shouldn't need to set anything else up.

**Info:** Inkscape Version 0.92 or greater, has a really key feature: the *Objects panel*.<br>
This gives you a heirarchical list of objects in your SVG file, listed in their stacking order. This is really important because the stacking order dictates the order that the shapes will be sewn in.<br><br>
Versions 0.92.2 and higher let you [bind a key](/docs/customize/#shortcut-keys) to new commands, “stack up” and “stack down”, which you can assign to pageup and pagedown. These let you arbitrarily reorder objects in the SVG file, which lets you directly manipulate which order they stitch in. It works way better than the default “raise” and “lower” commands.
{: .notice--info }

## Quick Setup

### 1. Download
Download the release archive for your platform.

The `LOCALE` selected affects the menus shown inside Inkscape. Ink/Stitch dialogs are in the lanugage of your OS (if that language is supported).

**Tip:** Your language is not available?<br>Help us to [translate the dialogs into your native language](/developers/localize/).
{: .notice--info }

Language|Linux (64bit)|Windows|macOS (Catalina) [[?]](#macos)
---|---|---|---
**English**|<i class="fa fa-download " ></i> [Linux]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-linux-en_US.zip)|<i class="fa fa-download " ></i> [Windows]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-windows-en_US.zip)|<i class="fa fa-download " ></i> [macOS]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-en_US.zip)|
**Finnish**|<i class="fa fa-download " ></i> [Linux]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-linux-fi_FI.zip)|<i class="fa fa-download " ></i> [Windows]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-windows-fi_FI.zip)|<i class="fa fa-download " ></i> [macOS]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-fi_FI.zip)|
**French**|<i class="fa fa-download " ></i> [Linux]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-linux-fr_FR.zip)|<i class="fa fa-download " ></i> [Windows]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-windows-fr_FR.zip)|<i class="fa fa-download " ></i> [macOS]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-fr_FR.zip)|
**German**|<i class="fa fa-download " ></i> [Linux]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-linux-de_DE.zip)|<i class="fa fa-download " ></i> [Windows]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-windows-de_DE.zip)|<i class="fa fa-download " ></i> [macOS]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-de_DE.zip)|
**Italian**|<i class="fa fa-download " ></i> [Linux]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-linux-it_IT.zip)|<i class="fa fa-download " ></i> [Windows]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-windows-it_IT.zip)|<i class="fa fa-download " ></i> [macOS]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-it_IT.zip)|
{: .inline-table }

**Latest release:** [Ink/Stitch {{ site.github.latest_release.tag_name }} ({{ site.github.latest_release.published_at | date: "%Y-%m-%d"  }})](https://github.com/inkstitch/inkstitch/releases/latest)

### 2. Install
 * In Inkscape 0.9, go to `Edit > Preferences > System` and check where your `User Extensions` folder is.
 * In Inkscape 1.0, go to `Inkscape > Preferences > System` and check where your `User Extensions` folder is.
 * Decompress the Ink/Stitch archive **directly** into this folder.<br />
   In this folder the file structure should look similiar to this (just a lot more files):
   ![File Structure](/assets/images/docs/en/file_structure.png)
 * Restart Inkscape.
 * You will then find Ink/Stitch under `Extensions > Ink/Stitch`.

#### Linux:

```
$ cd ~/.config/inkscape/extensions
$ unzip ~/Downloads/inkstitch-{{ site.github.latest_release.tag_name }}-linux-en_US.zip
```

#### macOS

macOS Catalina requires a special download method. If you download the Ink/Stitch release through the browser, you'll receive messages such as **"'xxxx' cannot be opened, because the developer cannot be verified"**. This happens because we did not pay Apple yearly for a developer id. You can avoid those messages by downloading Ink/Stitch with `curl` via Terminal App:

_for Inskscape 1.0 the `cd $directory` is different, please check and confirm the directory in your preferences_

```
$ cd ~/.config/inkscape/extensions
$ curl -LJO {{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-en_US.zip
$ unzip inkstitch-{{ site.github.latest_release.tag_name }}-osx-en_US.zip
```

**Info:** Ink/Stitch for macOS currently works only with **Catalina (10.15)**.<br>
If you have an older macOS version, get Ink/Stitch v1.26.2 (2019-08-20):
<br>**English:**
<i class="fa fa-download " ></i> [Sierra]({{ site.github.releases_url }}/download/v1.26.2/inkstitch-v1.26.2-osx-sierra-x86_64-en_US.tar.gz),
<i class="fa fa-download " ></i> [High Sierra]({{ site.github.releases_url }}/download/v1.26.2/inkstitch-v1.26.2-osx-high_sierra-x86_64-en_US.tar.gz),
<i class="fa fa-download " ></i> [Mojave]({{ site.github.releases_url }}/download/v1.26.2/inkstitch-v1.26.2-osx-mojave-x86_64-en_US.tar.gz)
<br>**French:**
<i class="fa fa-download " ></i> [Sierra]({{ site.github.releases_url }}/download/v1.26.2/inkstitch-v1.26.2-osx-sierra-x86_64-fr_FR.tar.gz),
<i class="fa fa-download " ></i> [High Sierra]({{ site.github.releases_url }}/download/v1.26.2/inkstitch-v1.26.2-osx-high_sierra-x86_64-fr_FR.tar.gz),
<i class="fa fa-download " ></i> [Mojave]({{ site.github.releases_url }}/download/v1.26.2/inkstitch-v1.26.2-osx-mojave-x86_64-fr_FR.tar.gz)
<br>**German:**
<i class="fa fa-download " ></i> [Sierra]({{ site.github.releases_url }}/download/v1.26.2/inkstitch-v1.26.2-osx-sierra-x86_64-de_DE.tar.gz),
<i class="fa fa-download " ></i> [High Sierra]({{ site.github.releases_url }}/download/v1.26.2/inkstitch-v1.26.2-osx-high_sierra-x86_64-de_DE.tar.gz),
<i class="fa fa-download " ></i> [Mojave]({{ site.github.releases_url }}/download/v1.26.2/inkstitch-v1.26.2-osx-mojave-x86_64-de_DE.tar.gz)
{: .notice--warning }

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
