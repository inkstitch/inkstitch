---
title: "Install Ink/Stitch on Linux"
permalink: /ru/docs/install-linux/
excerpt: "How to quickly install Ink/Stitch."
last_modified_at: 2021-05-03
toc: true
---
## Video Guide

We also provide beginner tutorial videos on our <i class="fab fa-youtube"></i> [YouTube channel](https://www.youtube.com/channel/UCJCDCFuT_xQoI55e10HRiRw). Watch the installation process for <i class="fab fa-linux"></i> [Linux](https://www.youtube.com/watch?v=Dkb5UvsZUNg&list=PLvlbfDmZyXG1ORmeqHdp4aP7J71e7icJP&index=2).

## Requirements

* [Inkscape](https://inkscape.org/release/) Version 1.0.2 or higher

That's it!  All python libraries and external dependencies are bundled (using the excellent [pyinstaller](http://www.pyinstaller.org)), so you shouldn't need to set anything else up.

## Installation

### Download
Download the release archive for your prefered language.

* <i class="fa fa-download " ></i> [английский]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-linux-en_US.zip)
* <i class="fa fa-download " ></i> [финский]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-linux-fi_FI.zip)
* <i class="fa fa-download " ></i> [Французский]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-linux-fr_FR.zip)
* <i class="fa fa-download " ></i> [Немецкий]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-linux-de_DE.zip)
* <i class="fa fa-download " ></i> [Японский]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-linux-ja_JP.zip)
* <i class="fa fa-download " ></i> [итальянский]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-linux-it_IT.zip)
* <i class="fa fa-download " ></i> [нидерландский]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-linux-nl_NL.zip)
* <i class="fa fa-download " ></i> [русский]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-linux-ru_RU.zip)

**Latest release:** {{ site.github.latest_release.published_at | date: "%d.%m.%Y"  }} [Ink/Stitch {{ site.github.latest_release.tag_name }}](https://github.com/inkstitch/inkstitch/releases/latest)

### Extract Files
Go to `Edit > Preferences > System` and check where your `User Extensions` folder is.

![Extensions folder location](/assets/images/docs/en/extensions-folder-location-linux.jpg)

Extract the Ink/Stitch archive into this folder.

```
$ cd ~/.config/inkscape/extensions
$ unzip ~/Downloads/inkstitch-{{ site.github.latest_release.tag_name }}-linux-en_US.zip
```

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

Check if you extracted Ink/Stitch into the correct folder. If the `User extensions folder` doesn't work out correctly, you can also try to install into the `Inkscape extensions folder`.
You can also look it up under `Edit > Preferences > System`.

**Confirm Ink/Stitch Version**

Verify if you have downloaded Ink/Stitch for Linux ([Download](#download))

**Confirm ownership/permissions**

Some users report false ownership/permissions can cause this issue.

### AttributeError: 'NoneType' object has no attribute 'title' in inkstitch.py

This error has been reported to us by users who have installed Inkscape through snap. Snap is known to cause issues for Ink/Stitch to run with Inkscape.
Please try an other installing method. Any described on [https://inkscape.org/](https://inkscape.org/releases/latest/) will be fine. 

### Ink/Stitch dialogs disappear after a few seconds

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
