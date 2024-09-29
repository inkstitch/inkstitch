---
title: Install Ink/Stitch on an Android Phone or Tablet
permalink: /tutorials/inkstistch-on-android/
last_modified_at: 2024-09-29
language: en
excerpt: "Install Ink/Stitch on Android with Termux"
image: "/assets/images/tutorials/android/android_inkstitch.png"

tutorial-type:
  - Text
after_footer_scripts:
  - /assets/js/copy_code.js
classes:
  - wide
---
![The simulator on a phone screen](/assets/images/tutorials/android/android_inkstitch_full.png)

Please note, that this is a fun tutorial. It is questionable how useful it is to use Ink/Stitch on a phone. The installation may crash often. We do not offer special support for it.
{: .notice--warning }

This tutorial is a bit technical and directed to experienced users. We will use Termux to setup a Linux Desktop on which we can use Inkscape and Ink/Stitch.

On this page you can find a simple installation walkthrough. More in depth information can be found here: [Termux](https://github.com/LinuxDroidMaster/Termux-Desktops), [Termux X11](https://github.com/termux/termux-x11)

We want to thank [LinuxDroidMaster](https://github.com/LinuxDroidMaster) for the hard work on the script which enables us to make this work.

## Install

In our example we are going to use proot, arch linux and xfce desktop. Read through the above mentioned documentation to decide what you want to use.
{: .notice--info }

* We start by installing [Termux](https://termux.dev/), if not already in use.

* In Termux install packages to run Linux for Termux and Android. Run these commands in Termux command line

  ```
  pkg update
  pkg upgrade
  ```

  ```
  pkg install x11-repo termux-x11-nightly tur-repo pulseaudio proot-distro wget git vim
  ```

* Download and install the termux-x11 app for Android from [termux-x11 nightly release](https://github.com/termux/termux-x11/releases/tag/nightly). Use the file `debug-universal.apk`.

* To install linux with proot-distro use the following command

  ```
  proot-distro install archlinux
  ```

* Login to archlinux container

  ```
  proot-distro login archlinux
  ```

* Now we are inside of the arch installation. Let's update the system

  ```
  pacman -Syu
  ```

* Install sudo

  ```
  pacman -S sudo
  ```

* Create user

  ```
  useradd -m -G wheel username
  passwd username
  ```

  Insert the following line into `/etc/sudoers`

  ```
  username ALL=(ALL) ALL
  ```

* Install xfce and inkscape. You can of course choose an other desktop environment if you want.

  ```
  pacman -S xfce4 inkscape
  ```

* Leave arch linux container

  ```
  exit
  ```

* Back in termux get the script to run the xfce

  ```
  wget https://raw.githubusercontent.com/LinuxDroidMaster/Termux-Desktops/main/scripts/proot_arch/startxfce4_arch.sh
  ```

  Make the script executable

  ```
  chmod +x startxfce4_arch.sh
  ```

  Edit the script to adapt it to your username

  ```
  vim startxfce4_arch.sh
  ```

  Replace the username `droidmaster` to your own username in this line

  ```
  proot-distro login archlinux --shared-tmp -- /bin/bash -c  'export PULSE_SERVER=127.0.0.1 && export XDG_RUNTIME_DIR=${TMPDIR} && su - droidmaster -c "env DISPLAY=:0 startxfce4"'
  ```

  On many phones you might encounter a black screen when the script is running.
  If this happens to you, replace `termux-x11 :0 >/dev/null &` with

  ```
  termux-x11 :0 -legacy-drawing >/dev/null &
  ```

  Save and exit vim

* Run the script and it will start up the xfce

  ```
  ./startxfce4_arch.sh
  ```

* We already installed Inkscape. So open it once, then close again.

  [Download Ink/Stitch for arm64](https://github.com/inkstitch/inkstitch-linux-arm64/releases/latest) and install as usual (copy to extensions folder).
