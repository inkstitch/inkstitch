---
title: "Install Ink/Stitch on Linux"
permalink: /docs/install-linux/
excerpt: "How to quickly install Ink/Stitch."
last_modified_at: 2025-06-17
toc: true
after_footer_scripts:
  - /assets/js/copy_code.js
---
{% comment %}
## Video Guide

We also provide beginner tutorial videos on our <i class="fab fa-youtube"></i> [YouTube channel](https://www.youtube.com/c/InkStitch). Watch the installation process for <i class="fab fa-linux"></i> [Linux](https://www.youtube.com/watch?v=Dkb5UvsZUNg&list=PLvlbfDmZyXG1ORmeqHdp4aP7J71e7icJP&index=2).
{% endcomment %}

## Requirements

Ink/Stitch is an Inkscape extension. Download and install [Inkscape](https://inkscape.org/release/) Version 1.0.2 or higher before you install Ink/Stitch.

## Installation

{% assign tag_name = site.github.latest_release.tag_name %}
Download the latest release (Ink/Stitch {{ tag_name }}) for Linux

{% assign tag_name = tag_name | slice: 1,tag_name.size %}

* x86_64:
  [tar.xz]({{ site.github.releases_url }}/latest/download/inkstitch-{{ tag_name }}-linux-x86_64.tar.xz),
  [sh]({{ site.github.releases_url }}/latest/download/inkstitch-{{ tag_name }}-linux-x86_64.sh),
  [rpm]({{ site.github.releases_url }}/latest/download/inkstitch-{{ tag_name }}-1.x86_64.rpm),
  [deb]({{ site.github.releases_url }}/latest/download/inkstitch_{{ tag_name }}_amd64.deb)
* i386:
  [tar.xz]({{ site.github.releases_url }}/latest/download/inkstitch-{{ tag_name }}-linux32-i386.tar.xz),
  [sh]({{ site.github.releases_url }}/latest/download/inkstitch-{{ tag_name }}-linux32-i386.sh),
  [rpm]({{ site.github.releases_url }}/latest/download/inkstitch-{{ tag_name }}-1.i386.rpm),
  [deb]({{ site.github.releases_url }}/latest/download/inkstitch_{{ tag_name }}_i386.deb)
* arm64:
  [tar.xz]({{ site.github.releases_url }}/latest/download/inkstitch-{{ tag_name }}-linux-aarch64.tar.xz),
  [sh]({{ site.github.releases_url }}/latest/download/inkstitch-{{ tag_name }}-linux-aarch64.sh),
  [rpm]({{ site.github.releases_url }}/latest/download/inkstitch-{{ tag_name }}-1.aarch64.rpm),
  [deb]({{ site.github.releases_url }}/latest/download/inkstitch_{{ tag_name }}_arm64.deb)
* Arch linux: <https://aur.archlinux.org/packages/inkstitch>
* NixOS: <https://search.nixos.org/packages?channel=unstable&show=inkscape-extensions.inkstitch>

**Latest release:** {{ site.github.latest_release.published_at | date: "%d.%m.%Y"  }} [Ink/Stitch {{ site.github.latest_release.tag_name }}](https://github.com/inkstitch/inkstitch/releases/latest)

### Install DEB and RPM

Double click on the downloaded deb file and follow the installation process.

RPM: [GPG-Key](/assets/files/inkstitch.gpg)

### Install SH

Use this version if you are using the AppImage version of Inkscape or if you just want to install Ink/Stitch only for your own user.
This script is also useful if your system doesn't support deb or rpm packages.

Open your terminal and navigate to the folder where the downloaded script is located and run the installer script, e.g.

```
cd Downloads
sh inkstitch-{{ tag_name }}-linux.sh
```

#### Expert options

This script will attempt to determine where to install Inkscape user extensions automatically.  If it gets it wrong, you can set one of these environment variables:

* `INKSCAPE_PATH` (ex: /usr/bin/inkscape)

  The path to the inkscape executable program.  This script will ask that program where to install extensions by passing it the `--user-data-directory` argument.

* `INKSCAPE_EXTENSIONS_PATH` (ex: $HOME/.config/inkscape/extensions)

  The path to the inkscape extensions directory.  Use this to bypass the --user-data-directory method and specify a directory yourself.

If you'd rather install it yourself, run this script with `--extract` to produce the original inkstitch-&lt;version&gt;.tar.xz file in the current directory.


### Install TAR.XZ

Go to `Edit > Preferences > System` and check where your `User Extensions` folder is.

![Extensions folder location](/assets/images/docs/en/extensions-folder-location-linux.jpg)

Extract the Ink/Stitch archive into this folder.

```
$ cd ~/.config/inkscape/extensions
$ tar -xvf ~/Downloads/inkstitch-{{ tag_name }}-linux.tar.xz
```

## Run Ink/Stitch

Open Inkscape.

You will then find Ink/Stitch under `Extensions > Ink/Stitch`.

## Update Ink/Stitch

### Recent Versions

If you want to update a `deb` or `rpm` install, just download the new package and run the installation as described above. It will replace the old installation.
The `installer script` will also remove the previously installed Ink/Stitch version before it installs Ink/Stitch.

This is only true for previous installation which used the same method. If you installed Ink/Stitch in an other way please follow the instructions for older updates first.

### Versions older than Ink/Stitch v2.1.0 or tar.xz version

Delete the old extension files first. Go to the extension directory and remove each inkstitch* file and folder.

Then, proceed as above.

The extensions directories can be seen in Inkscape under <code class="language-plaintext highlighter-rouge">Edit > Preferences > System</code>.

## Getting informed about Updates

Subscribe to a news feed channel to keep track on Ink/Stitch Updates:<br />
* <i class="fas fa-fw fa-rss-square" aria-hidden="true" style="color: #ffb400;"></i> [GitHub Feed on new Releases](https://github.com/inkstitch/inkstitch/releases.atom)
* <i class="fas fa-fw fa-rss-square" aria-hidden="true" style="color: #ffb400;"></i> [Ink/Stitch News](/feed.xml)
* <p>Or follow the project on GitHub <iframe style="display: inline-block;" src="https://ghbtns.com/github-btn.html?user=inkstitch&repo=inkstitch&type=watch&count=true&v=2" frameborder="0" scrolling="0" width="170px" height="20px"></iframe></p>

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

### Some Ink/Stitch dialogs disappear after a few seconds or don't show up at all

#### Use X11

This issue can be caused by wayland. Start Inkscape with the following command:

```
export GDK_BACKEND=x11 && inkscape
```

When using the Inkscape flatpak package, the command looks like this:

```
flatpak --env=GDK_BACKEND=x11 run org.inkscape.Inkscape
```

#### Extend timeout for mutter

In versions of mutter ≥ 3.35.92, you can set the timeout used to check if a
window is still alive. This is also useful for X-forwarding over ssh with
high latency.

For example, you can set the timeout to 60 s (60000 ms) using:

```gsettings set org.gnome.mutter check-alive-timeout 60000```

### ImportError: libnsl.so.1: cannot open shared object file. No such file or directory

Install the missing library.

For example on **Fedora** install libnsl with the following command

```
sudo dnf install libnsl
```

### I installed Ink/Stitch in my native language, but the dialogue windows are displayed in English

**Incomplete Translation**

It is possible, that not all strings have been translated. This is indicated by **some strings of text being in English and others in your native language**.
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
