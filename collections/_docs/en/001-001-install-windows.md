---
title: "Install Ink/Stitch on Windows"
permalink: /docs/install-windows/
excerpt: "How to quickly install Ink/Stitch."
last_modified_at: 2025-11-19
toc: true
---
{% comment %}
## Video Guide

We also provide beginner tutorial videos on our <i class="fab fa-youtube"></i> [YouTube channel](https://www.youtube.com/c/InkStitch). Watch the installation process for <i class="fab fa-windows"></i> [Windows](https://www.youtube.com/watch?v=U5htzWZSjA8&list=PLvlbfDmZyXG1ORmeqHdp4aP7J71e7icJP&index=4).
{% endcomment %}

## Requirements

Ink/Stitch is an Inkscape extension. Therefore, a current version of [Inkscape](https://inkscape.org/release/) (at least 1.0.2) must be installed before installation.

It's best to download Inkscape from the website. The Windows App Store version, in particular, might cause problems during the Ink/Stitch installation.

## Download

Use the button below to download the latest release.

<p><a href="{{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-windows-64bit.exe" class="btn btn--info btn--large"><i class="fa fa-download"></i> Download Ink/Stitch {{ site.github.latest_release.tag_name }} for Windows 64bit</a></p>

**Latest release:** {{ site.github.latest_release.published_at | date: "%Y-%m-%d"  }} [Ink/Stitch {{ site.github.latest_release.tag_name }}](https://github.com/inkstitch/inkstitch/releases/latest)

Free code signing provided by [SignPath.io](https://about.signpath.io) certificate by [SignPath Foundation](https://signpath.org).<br>See our [code signing policy](/code-signing-policy).
{: .notice--info }

### Tips for downloading using Microsoft Edge

Microsoft Edge may not download the file immediately or may pause the download. Follow these steps to complete the download.

* Select the download link (above).
* Edge shows a warning symbol. Select the symbol, then select the message text.

  ![Download warning message](/assets/images/docs/en/windows-download/01-warning-message.png)

* A bin icon and a menu button (ellipses) appear. Select the menu button.

  ![Download warning message with menu button](/assets/images/docs/en/windows-download/02-warning_message02.png)

* A small menu opens. Select `Keep`.

  ![Download warning message with menu](/assets/images/docs/en/windows-download/03-keep.png)

* Edge displays another warning. Select `Show more`.

  ![Another warning message](/assets/images/docs/en/windows-download/04-show-more.png)

* Three new options appear.

   If you want to help improve the download experience for future users, select `Report this app as safe`.

  Select `Keep anyway` to finish the download.

  ![Keep anyway option finally shows up](/assets/images/docs/en/windows-download/05-keep_anyway.png)

## Installation

Run the downloaded installer. 

Windows may block it from automatically running until the Windows certificate has gained enough trust. Until then, you will need to grant permission for the installer to run.

Select `More info` when this message appears.

![Ink/Stitch installer](/assets/images/docs/en/windows-install/installer01.png)

Select `Run anyway`.

![Ink/Stitch installer](/assets/images/docs/en/windows-install/installer02.png)

The installer will point to the Inkscape extensions folder automatically. The path is already set for you. You do not need to change this folder. Select `Next`.

![Ink/Stitch installer](/assets/images/docs/en/windows-install/installer03.png)

Since Inkscape is already installed, the extensions folder already exists. Select `Yes` to continue. 

![Ink/Stitch installer](/assets/images/docs/en/windows-install/installer04.png)

The installer shows you a summary of the installation settings. Select `Install`.

![Ink/Stitch installer](/assets/images/docs/en/windows-install/installer05.png)

When the process finishes, Ink/Stitch is ready to use.

![Ink/Stitch installer](/assets/images/docs/en/windows-install/installer06.png)

## Run Ink/Stitch

Open Inkscape to start using Ink/Stitch. You can find Ink/Stitch under `Extensions > Ink/Stitch`.

![Ink/Stitch menu](/assets/images/docs/en/windows-install/inkstitch-extensions-menu.png)

## Uninstall Ink/Stitch

### Uninstall Ink/Stitch (v2.1.0 and newer)

Open the start menu in Windows and select `Settings`.

![Uninstall Ink/Stitch](/assets/images/docs/en/windows-install/uninstall01.png)

Select `Apps`.

![Uninstall Ink/Stitch](/assets/images/docs/en/windows-install/uninstall02.png)

Scroll to Ink/Stitch.
Select `Ink/Stitch` and then select `Uninstall`.

![Uninstall Ink/Stitch](/assets/images/docs/en/windows-install/uninstall03.png)

Confirm that you want to uninstall Ink/Stitch.

![Uninstall Ink/Stitch](/assets/images/docs/en/windows-install/uninstall04.png)

Ink/Stitch has been removed from your computer. Click `Ok`.

![Uninstall Ink/Stitch](/assets/images/docs/en/windows-install/uninstall05.png)

### Uninstall Ink/Stitch versions older than v2.1.0

If you are using an older version of Ink/Stitch, you must manually remove it from the Inkscape extensions folder.

Open Inkscape and go to `Edit` then `Preferences`, then`System`. Select the button to open the extensions folder. Once it opens, find the the Ink/Stitch folder and delete it.  You may need to delete any subfolders and files first. 

![Inkscape extensions folder](/assets/images/docs/en/extensions-folder-location-win.jpg)

## Stay informed about Ink/Stitch updates

You can follow Ink/Stitch updates through our news feed or through the release feed on GitHub.

* <i class="fas fa-fw fa-rss-square" aria-hidden="true" style="color: #ffb400;"></i> [Ink/Stitch News (Website)](/feed.xml)<br />
* <i class="fas fa-fw fa-rss-square" aria-hidden="true" style="color: #ffb400;"></i> [New Releases on GitHub](https://github.com/inkstitch/inkstitch/releases.atom)<br>

<p>You can view project activity on GitHub if you want to stay updated on changes and development progress. <iframe style="display: inline-block;" src="https://ghbtns.com/github-btn.html?user=inkstitch&repo=inkstitch&type=watch&count=true&v=2" frameborder="0" scrolling="0" width="170px" height="20px"></iframe></p>

## Troubleshoot

This section covers common issues you may see when Ink/Stitch does not appear, when files are blocked by antivirus software, or when Inkscape cannot locate the correct folder. It also describes how to address Python path problems, Windows update issues, Windows 8 DLL messages, and language display problems.

### Error: Inkscape Extensions folder not found!

When your installation doesn't succeed and ends with the message `Error: Inkscape Extensions folder not found! Install and then run Inkscape to create the extension folder.`:

* Ensure, that you actually have Inkscape installed and opened and closed it at least once

If this message is still showing up, your Inkscape extensions folder might be at an uncommon location (or you are using the Windows App Store version of Inkscape).

* Download and install Inkscape from the [Inkscape website](https://inkscape.org/release/) (and run it at least once) before you try again
* or download the [Ink/Stitch zip file]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-windows-64bit.zip) and extract it to the Inkscape extensions folder

  You can find the extensions folder by opening Inkscape. Within Inkscape go to `Edit > Preferences > System`. This will show the system paths. In the line of `User extensions` click `open`.

### Ink/Stitch does not appear in the extension menu or is greyed out

**Antivirus Software**

Some antivirus tools may block Ink/Stitch because the installer uses a packed installer file. Add the Ink/Stitch extension folder to the exception list in your antivirus program, reinstall Ink/Stitch, then try again.

If your antivirus software deleted files, you may receive an error message like this:

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

### PYTHONPATH

There have been reports about an error message starting like this:

```
Python path configuration:
PYTHONHOME = 'C:\Users\{username}\AppData\Roaming\inkscape\extensions\inkstitch\bin'
PYTHONPATH = (not set)
```

Reinstall Inkscape. Confirm that "Add to path" is checked, when the PYTHONPATH question pops up during the installation.

### Windows 8: Error message

![The program can't start because api-ms-win-crt-math-l1-1-1-0.dll is missing from your computer. Try reinstalling the program to fix this problem](/assets/images/docs/en/windows-install/win8.png)
{: .img-half }
![Error loading Python DLL 'C:\Users\...\AppData\Roaming\inkscape\extensions\inkstitch\inkstitch\bin\python38.dll'. LoadLibrary: The specified module could not be found.](/assets/images/docs/en/windows-install/win8a.png)
{: .img-half }

If you come across these two error messages on Windows 8, download and install [Microsoft Visual C++ Redistributable packages](https://docs.microsoft.com/en-US/cpp/windows/latest-supported-vc-redist?view=msvc-170#visual-studio-2015-2017-2019-and-2022). Choose the file for your system architecture.

### Ink/Stitch is displayed in English

**Incomplete translations**

If Ink/Stitch is displayed in English, but you were expecting another language, the translations may be incomplete. This is indicated by **some strings of text displaying in English and others in the selected language**.
If you like to help complete the translation effort, please contribute here [description for translators](/developers/localize/).

**Language settings**

If Ink/Stitch cannot identify the language to display, it will use English.
You can set it directly in Inkscape. 
  * Go to Edit > Preferences > Interface (Ctrl + Shift + P)
  * Select the language
  * Restart Inkscape

![Preferences > Interface](/assets/images/docs/en/preferences_language.png)
