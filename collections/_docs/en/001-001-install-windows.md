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

<i class="fa fa-download " ></i> [Englisch]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-windows-en_US.zip) <i class="fa fa-download " ></i> [Finnish]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-windows-fi_FI.zip) <i class="fa fa-download " ></i> [French]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-windows-fr_FR.zip) <i class="fa fa-download " ></i> [German]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-windows-de_DE.zip) <i class="fa fa-download " ></i> [Italian]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-windows-it_IT.zip)

**Latest release:** {{ site.github.latest_release.published_at | date: "%Y-%m-%d"  }} [Ink/Stitch {{ site.github.latest_release.tag_name }}](https://github.com/inkstitch/inkstitch/releases/latest)

The `LOCALE` selected affects the menus shown inside Inkscape. Ink/Stitch dialogs are in the lanugage of your OS (if that language is supported).<br><br>Your language is not available? Help us to [translate the dialogs into your native language](/developers/localize/).
{: .notice--info }


### Extract Files

Go to `Edit > Preferences > System` (Inkscape 0.9) or `Inkscape > Preferences > System` (Inkscape 1.0) and check where your `User Extensions` folder is.

![Preferences: Extensions Folder](/assets/images/docs/en/extensions-folder-location-win.jpg)

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

## Troubleshoot

### Ink/Stitch doesn't show up / is greyed out

**Confirm installation path**

Check if files were possibly extracted into a *sub-directory*.
You should see a lot of files starting with "inkstitch" **directly** inside the extension folder, beside of one folder called "inkstitch".

**Antivirus Software**

Since Ink/Stitch is packed into a executable there are reports of anti-virus-software using heuristics that mark the extension as a false positive. The solution in this cases is to add the Ink/Stitch extension folder to the exception list on the av program and reinstall the extension and try again.

If your antivirus software deleted files, you will receive an error message like this:

```
Tried to launch: inkstitch\bin\inkstitch
  Arguments: ['inkstitch\bin\inkstitch', '--id=XXX', '--extension=XXX', 'C:\Users\XXX\AppData\Local\Temp\ink_ext_XXXXXX.svgXXXXX']
  Debugging information:

Traceback (most recent call last):
  File "inkstitch.py", line 35, in <module>
    extension = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  File "C:\Program Files\Inkscape\lib\python2.7/subprocess.py", line 325, in __init__ errread, errwrite)
  File "C:\Program Files\Inkscape\lib\python2.7/subprocess.py", line 575, in _execute_child startupinfo)
WindowsError: [Error 2] The system cannot find the file specified
```

**Confirm Ink/Stitch Version**

Verify if you have downloaded Ink/Stitch for Windows ([Download](#download))

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
