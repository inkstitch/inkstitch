---
title: "Install Ink/Stitch on Linux"
permalink: /docs/install-linux/
excerpt: "How to quickly install Ink/Stitch."
last_modified_at: 2020-12-03
toc: true
---
## Video Guide

We also provide beginner tutorial videos on our <i class="fab fa-youtube"></i> [YouTube channel](https://www.youtube.com/channel/UCJCDCFuT_xQoI55e10HRiRw). Watch the installation process for <i class="fab fa-linux"></i> [Linux](https://www.youtube.com/watch?v=Dkb5UvsZUNg&list=PLvlbfDmZyXG1ORmeqHdp4aP7J71e7icJP&index=2).

## Requirements

* [Inkscape](https://inkscape.org/) Version 0.92.2 or higher (including [Inkscape](https://inkscape.org/release/inkscape-1.0/?latest=1) Version 1.0.1)

That's it!  All python libraries and external dependencies are bundled (using the excellent [pyinstaller](http://www.pyinstaller.org)), so you shouldn't need to set anything else up.

## Installation

### Download
Download the release archive for your prefered language.

<i class="fa fa-download " ></i> [English]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-linux-en_US.zip) <i class="fa fa-download " ></i> [Finnish]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-linux-fi_FI.zip) <i class="fa fa-download " ></i> [French]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-linux-fr_FR.zip) <i class="fa fa-download " ></i> [German]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-linux-de_DE.zip) <i class="fa fa-download " ></i> [Italian]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-linux-it_IT.zip)

**Latest release:** {{ site.github.latest_release.published_at | date: "%d.%m.%Y"  }} [Ink/Stitch {{ site.github.latest_release.tag_name }}](https://github.com/inkstitch/inkstitch/releases/latest)

### Extract Files
Go to `Edit > Preferences > System` (Inkscape 0.9) or `Inkscape > Preferences > System` (Inkscape 1.0) and check where your `User Extensions` folder is.

![Extensions folder location](/assets/images/docs/en/extensions-folder-location-linux.jpg)

Extract the Ink/Stitch archive **directly** into this folder.

```
$ cd ~/.config/inkscape/extensions
$ unzip ~/Downloads/inkstitch-{{ site.github.latest_release.tag_name }}-linux-en_US.zip
```

The file structure should look similiar to this (just a lot more files):

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

## Troubleshoot

### Ink/Stitch doesn't run / is greyed out

**Confirm installation path**

Check if files were possibly extracted into a *sub-directory*.
You should see a lot of files starting with "inkstitch" **directly** inside the extension folder, beside of one folder called "inkstitch".

**Confirm Ink/Stitch Version**

Verify if you have downloaded Ink/Stitch for Linux ([Download](#download))

**Confirm ownership/permissions**

Some users report false ownership/permissions can cause this issue.

### AttributeError: 'NoneType' object has no attribute 'title' in inkstitch.py

This error has been reported to us by users who have installed Inkscape through snap. Snap is known to cause issues for Ink/Stitch to run with Inkscape.
Please try an other installing method. Any described on [https://inkscape.org/](https://inkscape.org/releases/latest/) will be fine. 

### Ink/Stitch dialogues disappear after a few seconds

This issue can be caused by wayland. Start Inkscape with the following command: `export GDK_BACKEND=x11 && inkscape`.

This workaround has to be used until we moved all Ink/Stitch applications to the electron environment. 

### I installed Ink/Stitch in my native language, but the dialogue windows are displayed in English

**Incomplete Translation**

It is possible, that not all strings have been translated. This is indicated by **some strings of text beeing in English and others in your native language**.
If you like to complete the translation, have a look at our [description for translators](/developers/localize/).

**Language Setting**

We have to distinguish between the Extension menu in Inkscape and the dialogue windows.
The selection of the ZIP file causes only the Extension menu to be in a certain language.
The dialgoue windows are build differently. They will use the language of your operating system.
If Ink/Stitch is uncertain, which language to support, it will fallback on English.
You can tell Inkscape explicitly to use your native language as follows:
  * Go to Edit > Preferences > Interface (Ctrl + Shift + P)
  * Set your language
  * Restart Inkscape

![Preferences > Interface](/assets/images/docs/en/preferences_language.png)
