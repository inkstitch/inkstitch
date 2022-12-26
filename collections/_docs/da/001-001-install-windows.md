---
title: "Install Ink/Stitch on Windows"
permalink: /da/docs/install-windows/
excerpt: "How to quickly install Ink/Stitch."
last_modified_at: 2022-04-24
toc: true
---
{% comment %}
## Video Guide

We also provide beginner tutorial videos on our <i class="fab fa-youtube"></i> [YouTube channel](https://www.youtube.com/c/InkStitch). Watch the installation process for <i class="fab fa-windows"></i> [Windows](https://www.youtube.com/watch?v=U5htzWZSjA8&list=PLvlbfDmZyXG1ORmeqHdp4aP7J71e7icJP&index=4).
{% endcomment %}

## Requirements

Ink/Stitch is an Inkscape extension. Download and install [Inkscape](https://inkscape.org/release/) Version 1.0.2 or higher before you install Ink/Stitch.

## Download

Download the latest release.

<p><a href="{{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-windows.exe" class="btn btn--info btn--large"><i class="fa fa-download " ></i> Download Ink/Stitch {{ site.github.latest_release.tag_name }} for Windows</a></p>

**Latest release:** {{ site.github.latest_release.published_at | date: "%Y-%m-%d"  }} [Ink/Stitch {{ site.github.latest_release.tag_name }}](https://github.com/inkstitch/inkstitch/releases/latest)

## Installation

Double click to execute the downloaded file.

Until our windows certificate gained enough trust, you will need to allow the installer script to run.

Click on `More info`.

![Ink/Stitch installer](/assets/images/docs/en/windows-install/installer01.png)

Now click on the additional option `Run anyway`.

![Ink/Stitch installer](/assets/images/docs/en/windows-install/installer02.png)

Ink/Stitch needs to be installed into the Inkscape extensions folder. The path is already set for you. Click on `Next`.

![Ink/Stitch installer](/assets/images/docs/en/windows-install/installer03.png)

Since you have Inkscape installed, the extensions folder already exists. Confirm that you want to install into this folder and click on `Yes`.

![Ink/Stitch installer](/assets/images/docs/en/windows-install/installer04.png)

The installer will show you a summary of the installation settings. Click on `Install`.

![Ink/Stitch installer](/assets/images/docs/en/windows-install/installer05.png)

Ink/Stitch is now installed on your computer.

![Ink/Stitch installer](/assets/images/docs/en/windows-install/installer06.png)

## Run Ink/Stitch

Open Inkscape. You will find Ink/Stitch under `Extensions > Ink/Stitch`.

![Ink/Stitch menu](/assets/images/docs/en/windows-install/inkstitch-extensions-menu.png)

## Uninstall Ink/Stitch

### Uninstall Ink/Stitch versions up from v2.1.0

Open the start menu in Windows. Click on `Settings`.

![Uninstall Ink/Stitch](/assets/images/docs/en/windows-install/uninstall01.png)

Click on `Apps`.

![Uninstall Ink/Stitch](/assets/images/docs/en/windows-install/uninstall02.png)

In `Apps & features` scroll down until you find Ink/Stitch.
Click on `Ink/Stitch` and an uninstall button appears. Click on `Uninstall`.

![Uninstall Ink/Stitch](/assets/images/docs/en/windows-install/uninstall03.png)

Confirm that you want to uninstall Ink/Stitch.

![Uninstall Ink/Stitch](/assets/images/docs/en/windows-install/uninstall04.png)

Ink/Stitch has been removed from your computer. Click `Ok`.

![Uninstall Ink/Stitch](/assets/images/docs/en/windows-install/uninstall05.png)

### Uninstall Ink/Stitch versions older than v2.1.0

Go to `Edit > Preferences > System` and open your extensions folder.

![Inkscape extensions folder](/assets/images/docs/en/extensions-folder-location-win.jpg)

Remove each inkstitch* file and folder.

## Get informed about Ink/Stitch updates

Subscribe to a news feed channel to keep track on Ink/Stitch Updates.

* <i class="fas fa-fw fa-rss-square" aria-hidden="true" style="color: #ffb400;"></i> [Ink/Stitch News (Website)](/feed.xml)<br />
* <i class="fas fa-fw fa-rss-square" aria-hidden="true" style="color: #ffb400;"></i> [New Releases on GitHub](https://github.com/inkstitch/inkstitch/releases.atom)<br>

<p>Alternatively watch all project activity on GitHub: <iframe style="display: inline-block;" src="https://ghbtns.com/github-btn.html?user=inkstitch&repo=inkstitch&type=watch&count=true&v=2" frameborder="0" scrolling="0" width="170px" height="20px"></iframe></p>

## Troubleshoot

### Ink/Stitch doesn't show up / is greyed out

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

**Confirm installation path**

Check if you extracted Ink/Stitch into the correct folder. If the `User extensions folder` doesn't work out correctly, you can also try to install into the `Inkscape extensions folder`.
You can also look it up under `Edit > Preferences > System`.

### PYTHONPATH

There have been reports about an error message starting like this:

```
Python path configuration:
PYTHONHOME = 'C:\Users\{username}\AppData\Roaming\inkscape\extensions\inkstitch\bin'
PYTHONPATH = (not set)
```

Reinstall Inkscape. Make sure that "Add to path" is checked, when the PYTHONPATH question pops up during the installation.

### Windows 7: Error message

When you see the following error message please install Microsoft Windows security updates on your computer.

```
Traceback (most recent call last):
File "Lib\site-packages\PyInstaller\hooks\rthooks\pyi_rth_multiprocessing.py", line 12, in
File "PyInstaller\loader\pyimod03_importers.py", line 495, in exec_module
File "multiprocessing_init_.py", line 16, in
File "PyInstaller\loader\pyimod03_importers.py", line 495, in exec_module
File "multiprocessing\context.py", line 6, in
File "PyInstaller\loader\pyimod03_importers.py", line 495, in exec_module
File "multiprocessing\reduction.py", line 16, in
File "PyInstaller\loader\pyimod03_importers.py", line 495, in exec_module
File "socket.py", line 49, in
ImportError: DLL load failed while importing _socket: Paramètre incorrect.
```

### Windows 8: Error message

![The program can't start because api-ms-win-crt-math-l1-1-1-0.dll is missing from your computer. Try reinstalling the program to fix this problem](/assets/images/docs/en/windows-install/win8.png)
{: .img-half }
![Error loading Python DLL 'C:\Users\...\AppData\Roaming\inkscape\extensions\inkstitch\inkstitch\bin\python38.dll'. LoadLibrary: The specified module could not be found.](/assets/images/docs/en/windows-install/win8a.png)
{: .img-half }

If you come across these two error messages on Windows 8, download and install [Microsoft Visual C++ Redistributable packages](https://docs.microsoft.com/en-US/cpp/windows/latest-supported-vc-redist?view=msvc-170#visual-studio-2015-2017-2019-and-2022). Choose the file for your system architecture.

### Ink/Stitch is displayed in English

**Incomplete Translation**

It is possible, that not all strings have been translated. This is indicated by **some strings of text beeing in English and others in your native language**.
If you like to complete the translation, have a look at our [description for translators](/developers/localize/).

**Language Settings**

If Ink/Stitch is uncertain, which language to support, it will fallback on English.
You can tell Inkscape explicitly to use your native language as follows:
  * Go to Edit > Preferences > Interface (Ctrl + Shift + P)
  * Set your language
  * Restart Inkscape

![Preferences > Interface](/assets/images/docs/en/preferences_language.png)
