---
title: "Install Ink/Stitch on macOS"
permalink: /docs/install-macos/
excerpt: "How to quickly install Ink/Stitch."
last_modified_at: 2020-12-03
toc: true
---
## Video Guide

We also provide beginner tutorial videos on our <i class="fab fa-youtube"></i> [YouTube channel](https://www.youtube.com/channel/UCJCDCFuT_xQoI55e10HRiRw). Watch the installation process for <i class="fab fa-apple"></i> [macOS](https://www.youtube.com/watch?v=gmOVLNh9cu8&list=PLvlbfDmZyXG1ORmeqHdp4aP7J71e7icJP&index=3).

**Warning:** The video for macOS users is outdated. Please read updated info ["Additional Steps for Catalina and Big Sur"](#addtitional-steps-for-catalina--big-sur)
{: .notice--warning }

## Requirements

* [Inkscape](https://inkscape.org/) Version 0.92.2 or higher (including [Inkscape](https://inkscape.org/release/inkscape-1.0/?latest=1) Version 1.0.1)

That's it!  All python libraries and external dependencies are bundled (using the excellent [pyinstaller](http://www.pyinstaller.org)), so you shouldn't need to set anything else up.

## Installation

### Download
Download the release archive.

Language|macOS Catalina / Big Sur | Sierra* | High Sierra* | Mojave*
---|---|---|---
**English**|<i class="fa fa-download " ></i> [Catalina / Big Sur]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-en_US.zip)|<i class="fa fa-download " ></i> [Sierra]({{ site.github.releases_url }}/download/v1.26.2/inkstitch-v1.26.2-osx-sierra-x86_64-en_US.tar.gz)|<i class="fa fa-download " ></i> [High Sierra]({{ site.github.releases_url }}/download/v1.26.2/inkstitch-v1.26.2-osx-high_sierra-x86_64-en_US.tar.gz)|<i class="fa fa-download " ></i> [Mojave]({{ site.github.releases_url }}/download/v1.26.2/inkstitch-v1.26.2-osx-mojave-x86_64-en_US.tar.gz)|
**Finnish**|<i class="fa fa-download " ></i> [Catalina / Big Sur]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-fi_FI.zip)|
**French**|<i class="fa fa-download " ></i> [Catalina / Big Sur]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-fr_FR.zip)|<i class="fa fa-download " ></i> [Sierra]({{ site.github.releases_url }}/download/v1.26.2/inkstitch-v1.26.2-osx-sierra-x86_64-fr_FR.tar.gz)|<i class="fa fa-download " ></i> [High Sierra]({{ site.github.releases_url }}/download/v1.26.2/inkstitch-v1.26.2-osx-high_sierra-x86_64-fr_FR.tar.gz)|<i class="fa fa-download " ></i> [Mojave]({{ site.github.releases_url }}/download/v1.26.2/inkstitch-v1.26.2-osx-mojave-x86_64-fr_FR.tar.gz)|
**German**|<i class="fa fa-download " ></i> [Catalina / Big Sur]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-de_DE.zip)|<i class="fa fa-download " ></i> [Sierra]({{ site.github.releases_url }}/download/v1.26.2/inkstitch-v1.26.2-osx-sierra-x86_64-de_DE.tar.gz)|<i class="fa fa-download " ></i> [High Sierra]({{ site.github.releases_url }}/download/v1.26.2/inkstitch-v1.26.2-osx-high_sierra-x86_64-de_DE.tar.gz)|<i class="fa fa-download " ></i> [Mojave]({{ site.github.releases_url }}/download/v1.26.2/inkstitch-v1.26.2-osx-mojave-x86_64-de_DE.tar.gz)|
**Italian**|<i class="fa fa-download " ></i> [Catalina / Big Sur]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-it_IT.zip)|
{: .inline-table }

\* There are no recent versions of Ink/Stitch for Sierra, High Sierra or Mojave. The files are from an older Ink/Stitch release: Ink/Stitch v1.26.2 (2019-08-20).

**Latest release:** [Ink/Stitch {{ site.github.latest_release.tag_name }} ({{ site.github.latest_release.published_at | date: "%Y-%m-%d"  }})](https://github.com/inkstitch/inkstitch/releases/latest)

The `LOCALE` selected affects the menus shown inside Inkscape. Ink/Stitch dialogs are in the lanugage of your OS (if that language is supported).<br><br>Your language is not available? Help us to [translate the dialogs into your native language](/developers/localize/).
{: .notice--info }

### Extract Files

Go to `Edit > Preferences > System` (Inkscape 0.9) or `Inkscape > Preferences > System` (Inkscape 1.0) and check where your `User Extensions` folder is.

![Preferences: Extensions Folder](/assets/images/docs/en/extensions-folder-localtion-mac.jpg)
  
Extract the Ink/Stitch archive **directly** into this folder. In this folder the file structure should look similiar to this (just a lot more files):

![File Structure](/assets/images/docs/en/file_structure.png)

### Addtitional Steps for Catalina / Big Sur

Newer macOS versions will complain about Ink/Stitch if it is downloaded through your browser. You will receive an error message like this: `'xxxx' cannot be opened, because the developer cannot be verified`.

To avoid this error message open your Terminal App. Click on the small magnifying glass icon in your menu bar in the top right corner (or press <key>Command (⌘)</key>+<key>Space</key>). Search for `Terminal` and open the application.

In the Terminal enter the following command:

```
xattr -r -d com.apple.quarantine ~/Library/Application\ Support/org.inkscape.Inkscape/config/inkscape/extensions/
```

Replace `~/Library/Application\ Support/org.inkscape.Inkscape/config/inkscape/extensions/` if your Inkscape extension folder path has an other location (verify through `Inkscape > Preferences > System`).

Users of **Big Sur** will need to do one further step to complete the installation:

```
cd ~/Library/Application\ Support/org.inkscape.Inkscape/config/inkscape/extensions/
cd inkstitch/bin
ln -s libpython2.7.dylib libc.dylib #Any random dylib should work, libpython2.7 is just a convenient one in the directory. 
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
