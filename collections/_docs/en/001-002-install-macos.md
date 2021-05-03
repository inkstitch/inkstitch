---
title: "Install Ink/Stitch on macOS"
permalink: /docs/install-macos/
excerpt: "How to quickly install Ink/Stitch."
last_modified_at: 2021-05-03
toc: true
---
## Video Guide

We also provide beginner tutorial videos on our <i class="fab fa-youtube"></i> [YouTube channel](https://www.youtube.com/channel/UCJCDCFuT_xQoI55e10HRiRw). Watch the installation process for <i class="fab fa-apple"></i> [macOS](https://www.youtube.com/watch?v=gmOVLNh9cu8&list=PLvlbfDmZyXG1ORmeqHdp4aP7J71e7icJP&index=3).

**Warning:** The video for macOS users is outdated. Please read updated info ["Additional Steps for Catalina and Big Sur"](#addtitional-steps-for-catalina--big-sur)
{: .notice--warning }

## Requirements

* [Inkscape](https://inkscape.org/release/) Version 1.0.2 or higher

That's it!  All python libraries and external dependencies are bundled (using the excellent [pyinstaller](http://www.pyinstaller.org)), so you shouldn't need to set anything else up.

## Installation

### Download
Download the release archive.

Language| Catalina & Big Sur | High Sierra & Mojave | Sierra & El Capitan
---|---|---|---
**Dutch** | <i class="fa fa-download " ></i> [Catalina / Big Sur]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-nl_NL.zip) | <i class="fa fa-download " ></i> [High Sierra / Mojave]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-mojave-nl_NL.tar.gz)|<i class="fa fa-download " ></i> [Sierra / El Capitan]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-sierra-nl_NL.tar.gz)|
**English** | <i class="fa fa-download " ></i> [Catalina / Big Sur]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-en_US.zip) | <i class="fa fa-download " ></i> [High Sierra / Mojave]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-mojave-en_US.tar.gz)|<i class="fa fa-download " ></i> [Sierra / El Capitan]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-sierra-en_US.tar.gz)|
**Finnish** | <i class="fa fa-download " ></i> [Catalina / Big Sur]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-fi_FI.zip) | <i class="fa fa-download " ></i> [High Sierra / Mojave]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-mojave-fi_FI.tar.gz)|<i class="fa fa-download " ></i> [Sierra / El Capitan]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-sierra-fi_FI.tar.gz)|
**French** | <i class="fa fa-download " ></i> [Catalina / Big Sur]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-fr_FR.zip) | <i class="fa fa-download " ></i> [High Sierra / Mojave]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-mojave-fr_FR.tar.gz)|<i class="fa fa-download " ></i> [Sierra / El Capitan]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-sierra-fr_FR.tar.gz)|
**German** | <i class="fa fa-download " ></i> [Catalina / Big Sur]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-de_DE.zip) | <i class="fa fa-download " ></i> [High Sierra / Mojave]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-mojave-de_DE.tar.gz)|<i class="fa fa-download " ></i> [Sierra / El Capitan]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-sierra-de_DE.tar.gz)
**Italian** | <i class="fa fa-download " ></i> [Catalina / Big Sur]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-it_IT.zip) | <i class="fa fa-download " ></i> [High Sierra / Mojave]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-mojave-it_IT.tar.gz)|<i class="fa fa-download " ></i> [Sierra / El Capitan]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-sierra-it_IT.tar.gz)
**Japanese** | <i class="fa fa-download " ></i> [Catalina / Big Sur]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-ja_JP.zip) | <i class="fa fa-download " ></i> [High Sierra / Mojave]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-mojave-ja_JP.tar.gz)|<i class="fa fa-download " ></i> [Sierra / El Capitan]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-sierra-ja_JP.tar.gz)
**Russian** | <i class="fa fa-download " ></i> [Catalina / Big Sur]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-ru_RU.zip) | <i class="fa fa-download " ></i> [High Sierra / Mojave]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-mojave-ru_RU.tar.gz)|<i class="fa fa-download " ></i> [Sierra / El Capitan]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-sierra-ru_RU.tar.gz)
{: .inline-table }

**Latest release:** [Ink/Stitch {{ site.github.latest_release.tag_name }} ({{ site.github.latest_release.published_at | date: "%Y-%m-%d"  }})](https://github.com/inkstitch/inkstitch/releases/latest)

The `LOCALE` selected affects the menus shown inside Inkscape. Ink/Stitch dialogs are in the lanugage of your OS (if that language is supported).<br><br>Your language is not available? Help us to [translate the dialogs into your native language](/developers/localize/).
{: .notice--info }

### Extract Files

Go to `Edit > Preferences > System` and check where your `User Extensions` folder is.

![Preferences: Extensions Folder](/assets/images/docs/en/extensions-folder-location-macos.jpg)
  
Extract the Ink/Stitch archive into this folder.

### Addtitional Steps for Catalina / Big Sur

Newer macOS versions will complain about Ink/Stitch if it is downloaded through your browser. You will receive an error message like this: `'xxxx' cannot be opened, because the developer cannot be verified`.

To avoid this error message open your Terminal App. Click on the small magnifying glass icon in your menu bar at the top right corner (or press <key>Command (⌘)</key>+<key>Space</key>). Search for `Terminal` and open the application.

In the Terminal enter the following command:

```
xattr -r -d com.apple.quarantine ~/Library/Application\ Support/org.inkscape.Inkscape/config/inkscape/extensions/
```

Replace `~/Library/Application\ Support/org.inkscape.Inkscape/config/inkscape/extensions/` if your Inkscape extension folder path has an other location (verify through `Inkscape > Preferences > System`).

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
You can also look it up under `Inkscape > Preferences > System`.

**Confirm version**

Please verify if you have downloaded Ink/Stitch for macOS ([Download](#download)).

### 'xxxx' cannot be opened, because the developer cannot be verified

Read ["Additional Steps for Catalina and Big Sur"](#addtitional-steps-for-catalina--big-sur).

### ValueError: Null geometry supports no operations

Ink/Stitch on macOS could raise the following error message:  `[...] ValueError: Null geometry supports no operations`.

This error is caused by an incompatibality of the shapely speedups library, which is inlcuded in the Ink/Stitch files.
In order to bring Ink/Stitch back to work delete the library as follows:

* Open the folder of your Ink/Stitch installation (usually this is: `~/Library/Application\ Support/org.inkscape.Inkscape/config/inkscape/extensions/`)
* Open as well your Ink/Stitch subfolder if you have one
* Press `Ctrl` while you click on the inkstitch application file and select Show `Package Contents` 

  ![Show Package Contents](/assets/images/docs/en/macOS-nogeometry.png)

* Go into the Folder `Contents > MacOS` and delete the folder named `shapely`

### I installed Ink/Stitch in my native language, but the dialogue windows are displayed in English

**Incomplete Translation**

It is possible, that not all strings have been translated. This is indicated by **some strings of text beeing in English and others in your native language**.
If you like to complete the translation, have a look at our [description for translators](/developers/localize/).

**Language Settings**

We have to distinguish between the Extension menu in Inkscape and the dialogue windows.
The selection of the ZIP file causes only the Extension menu to be in a certain language.
The dialgoue windows are build differently. They will use the language of your operating system.
If Ink/Stitch is uncertain, which language to support, it will fallback on English.
You can tell Inkscape explicitly to use your native language as follows:
  * Go to Edit > Preferences > Interface (Ctrl + Shift + P)
  * Set your language
  * Restart Inkscape

![Preferences > Interface](/assets/images/docs/en/preferences_language.png)
