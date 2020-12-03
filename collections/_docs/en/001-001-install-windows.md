---
title: "Install Ink/Stitch on Windows"
permalink: /docs/install-windows/
excerpt: "How to quickly install Ink/Stitch."
last_modified_at: 2020-12-03
toc: true
---
## Video Guide

We also provide beginner tutorial videos on our <i class="fab fa-youtube"></i> [YouTube channel](https://www.youtube.com/channel/UCJCDCFuT_xQoI55e10HRiRw). Watch the installation process for <i class="fab fa-windows"></i> [Windows](https://www.youtube.com/watch?v=U5htzWZSjA8&list=PLvlbfDmZyXG1ORmeqHdp4aP7J71e7icJP&index=4).

## Requirements

* [Inkscape](https://inkscape.org/) Version 0.92.2 or higher (including [Inkscape](https://inkscape.org/release/inkscape-1.0/?latest=1) Version 1.0.1)

That's it!  All python libraries and external dependencies are bundled (using the excellent [pyinstaller](http://www.pyinstaller.org)), so you shouldn't need to set anything else up.

## Installation

### Download
Download the release archive in your prefered language:

<i class="fa fa-download " ></i> [Englisch]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-windows-en_US.zip) <i class="fa fa-download " ></i> [Finnish]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-windows-fi_FI.zip), <i class="fa fa-download " ></i> [French]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-windows-fr_FR.zip) <i class="fa fa-download " ></i> [German]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-windows-de_DE.zip) <i class="fa fa-download " ></i> [Italian]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-windows-it_IT.zip)

**Latest release:** {{ site.github.latest_release.published_at | date: "%Y-%m-%d"  }} [Ink/Stitch {{ site.github.latest_release.tag_name }}](https://github.com/inkstitch/inkstitch/releases/latest)

The `LOCALE` selected affects the menus shown inside Inkscape. Ink/Stitch dialogs are in the lanugage of your OS (if that language is supported).<br><br>Your language is not available? Help us to [translate the dialogs into your native language](/developers/localize/).
{: .notice--info }


### Extract Files

Go to `Edit > Preferences > System` (Inkscape 0.9) or `Inkscape > Preferences > System` (Inkscape 1.0) and check where your `User Extensions` folder is.

![Preferences: Extensions Folder](/assets/images/docs/en/extensions-folder-localtion-mac.jpg)

Your folder will most likely look like this `C:\Users\%USERNAME%\AppData\Roaming\inkscape\extensions`

Extract the Ink/Stitch archive **directly** into this folder. The file structure should look similiar to this (just a lot more files):

![File Structure](/assets/images/docs/en/file_structure.png)

### Run Ink/Stitch

Restart Inkscape.

You will then find Ink/Stitch under `Extensions > Ink/Stitch`.

## Upgrade

Delete the old extension files first. Go to the extension directory and remove each inkstitch* file and folder.

Then, proceed as above.

**Tip:** Subscribe to a news feed channel to keep track on Ink/Stitch Updates:<br />
 <i class="fas fa-fw fa-rss-square" aria-hidden="true" style="color: #ffb400;"></i> [GitHub Feed on new Releases](https://github.com/inkstitch/inkstitch/releases.atom)<br>
 <i class="fas fa-fw fa-rss-square" aria-hidden="true" style="color: #ffb400;"></i> [Ink/Stitch News](/feed.xml)<br />
{: .notice--info }

<p class="notice--info" style="margin-top: -3.5em !important;">Or watch the project on GitHub:<br /><iframe style="display: inline-block;" src="https://ghbtns.com/github-btn.html?user=inkstitch&repo=inkstitch&type=watch&count=true&v=2" frameborder="0" scrolling="0" width="170px" height="20px"></iframe></p>
