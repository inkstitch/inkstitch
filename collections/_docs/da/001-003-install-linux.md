---
title: "Install Ink/Stitch on Linux"
permalink: /da/docs/install-linux/
excerpt: "How to quickly install Ink/Stitch."
last_modified_at: 2022-01-08
toc: true
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

<div class="instructions">
  <p class="download-button"><a href="{{ site.github.releases_url }}/latest/download/inkstitch_{{ tag_name }}_amd64.deb" class="btn btn--info btn--large"><i class="fa fa-download " ></i> Download DEB package</a></p>
  <input type="checkbox" id="deb-instructions" />
  <label for="deb-instructions">Installation instructions <p class="down">▿</p><p class="up">▵</p></label>
  <section>
    <p class="headline">Install deb package</p>
    <p>Double click on the downloaded deb file and follow the installation process.</p>
  </section>
</div>

<div class="instructions">
  <p class="download-button"><a href="{{ site.github.releases_url }}/latest/download/inkstitch-{{ tag_name }}-1.x86_64.rpm" class="btn btn--info btn--large"><i class="fa fa-download " ></i> Download RPM package</a></p>
  <input type="checkbox" id="rpm-instructions" />
  <label for="rpm-instructions">Installation instructions <p class="down">▿</p><p class="up">▵</p></label>
  <section>
    <p class="headline">Install rpm package</p>
    <p>Double click on the downloaded rpm file and follow the installation process.</p>
    <p><a href="/assets/files/inkstitch.gpg">GPG-Key</a></p>
  </section>
</div>

<div class="instructions">
  <p class="download-button"><a href="{{ site.github.releases_url }}/latest/download/inkstitch-{{ tag_name }}-linux.sh" class="btn btn--info btn--large"><i class="fa fa-download " ></i> Download installer script</a></p>
  <input type="checkbox" id="installer-instructions" />
  <label for="installer-instructions">Installation instructions <p class="down">▿</p><p class="up">▵</p></label>
  <section>
    <p class="headline"> Install with the installer script</p>
    <p>Use this version if you are using the AppImage version of Inkscape or if you just want to install Ink/Stitch only for your own user. This script is also useful if your system doesn't support deb or rpm packages.</p>
    <p>Open your terminal and navigate to the folder where the downloaded script is located, e.g.</p>
    <div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>cd Downloads</code></pre></div></div>
    <p>Run the following command</p>
    <div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>sh inkstitch-{{ tag_name }}-linux.sh</code></pre></div></div>
    <p><b>Expert options</b></p>
    <p>This script will attempt to determine where to install Inkscape user extensions automatically.  If it gets it wrong, you can set one of these environment variables:</p>
    <ul>
      <li>
        <p><code class="language-plaintext highlighter-rouge">INKSCAPE_PATH (ex: /usr/bin/inkscape)</code></p>
        <p>The path to the inkscape executable program.  This script will ask that program where to install extensions by passing it the --user-data-directory argument.</p>
      </li>
      <li>
        <p><code class="language-plaintext highlighter-rouge">INKSCAPE_EXTENSIONS_PATH (ex: $HOME/.config/inkscape/extensions)</code></p>
        <p>The path to the inkscape extensions directory.  Use this to bypass the --user-data-directory method and specify a directory yourself.</p>
      </li>
    </ul>
    <p>If you'd rather install it yourself, run this script with <code class="language-plaintext highlighter-rouge">--extract</code> to produce the original inkstitch-&lt;version&gt;.tar.xz file in the current directory.</p>
  </section>
</div>

<div class="instructions">
  <p class="download-button"><a href="{{ site.github.releases_url }}/latest/download/inkstitch-{{ tag_name }}-linux.tar.xz" class="btn btn--info btn--large"><i class="fa fa-download " ></i> Download tar.xz archive</a></p>
  <input type="checkbox" id="archive-instructions" />
  <label for="archive-instructions">Installation instructions <p class="down">▿</p><p class="up">▵</p></label>
  <section>
  <p class="headline">Install with tar.xz archive</p>
  <p>Go to <code class="language-plaintext highlighter-rouge">Edit > Preferences > System</code> and check where your <code class="language-plaintext highlighter-rouge">User Extensions</code> folder is.</p>
  <p><img alt="Extensions folder location" src="/assets/images/docs/en/extensions-folder-location-linux.jpg" /></p>
  <p>Extract the Ink/Stitch archive into this folder.</p>
  <div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>$ cd ~/.config/inkscape/extensions
$ tar -xvf ~/Downloads/inkstitch-{{ tag_name }}-linux.tar.xz</code></pre></div></div>
  </section>
</div>

**Latest release:** {{ site.github.latest_release.published_at | date: "%d.%m.%Y"  }} [Ink/Stitch {{ site.github.latest_release.tag_name }}](https://github.com/inkstitch/inkstitch/releases/latest)

## Run Ink/Stitch
Restart Inkscape.

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

### Ink/Stitch dialogs disappear after a few seconds

This issue can be caused by wayland. Start Inkscape with the following command: `export GDK_BACKEND=x11 && inkscape`.

This workaround has to be used until we moved all Ink/Stitch applications to the electron environment. 

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
