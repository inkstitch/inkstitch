---
title: "Windows Manual Build"
permalink: /da/developers/inkstitch/windows-manual-build/
last_modified_at: 2022-02-01
toc: true
---
This is an instructional guide how to build Ink/Stitch without using the manual install.

**Info:** For this description we use **`foo`** as a user name. Whenever it occures **replace it** with your personal windows user name.
{: .notice--warning }

## Requirements

Install these dependancies to build a local build of inkstitch for windows.

* [Build Tools for Visual Studio 2022](https://visualstudio.microsoft.com/de/downloads/)
  * Scroll down on their website until you see "Tools for Visual Studio 2022" and open the submenu
  * Scroll down again and download "Buildtools for Visual Studio 2022"
  * Run the installation
    ![Click on modify](/assets/images/developers/windows-manual-build/build-tools-modify.png)
    ![Select desktop development with c++](/assets/images/developers/windows-manual-build/windows_build-tools.png)
* [Python](https://www.python.org/downloads/release/python-398/)

  Choose the 32bit version, run the installer and check "Add Python x.xx to PATH".
  This for the bash enviroment to find python.
  ![Add python to path](/assets/images/developers/windows-manual-build/Python.png)
  Then click on "Install now"
* [Git for windows](https://gitforwindows.org/)

  This installs git as well as providing a terminal emulator to run build scripts.

  Download 
  Use the default settings during installation.
* [nodejs](https://nodejs.org/en/download/)

  Install LTS 32 bit version. Install with default settings.

* [Inno setup](https://jrsoftware.org/isdl.php)

  This provides the compiler to build the windows installer.
  Use the default settings.
* [make](https://sourceforge.net/projects/mingw-w64/files/External%20binary%20packages%20%28Win64%20hosted%29/make/)

  This provides make to run the build scripts.
  * Download make-3.82.90-20111115.zip
  * unzip
  * Create the folder C:\Make\bin
  * Copy `make.exe` from `Downloads\make-3.82.90-20111115\make-3.82.90-20111115\bin_ix86` to `C:\Make\bin`

  ![Make folder with make.exe](/assets/images/developers/windows-manual-build/make-path.png)

## PATHS

The bash environment needs some paths for the installed software. So let's set it up.

* Open Windows settings > System > About > Advanced system settings 

  ![Windows settings](/assets/images/developers/windows-manual-build/WindowsSystem.png)

  ![About](/assets/images/developers/windows-manual-build/PATH1.png)

* In Advanced Settings click on `Enviroment Vairables`

  ![Advanced Settings](/assets/images/developers/windows-manual-build/PATH2.png)

* In `User variables for [foo]` click on Path (1) and then on `Edit...` (2)

  ![Environment Variables](/assets/images/developers/windows-manual-build/PATH3.png)

* For each of the paths below click on `New` then copy paste the file path:

  ```
  C:\Make\bin
  C:\Program Files (x86)\Inno Setup 6
  ```
* Now it should look like this:

  ![Environment Variables](/assets/images/developers/windows-manual-build/Final-paths.png)

## Download Ink/Stitch

* Create a folder where you want to keep your Ink/Stitch source files
* Right click into the file browser and click on `Git Bash Here`

  ![Right click menu](/assets/images/developers/windows-manual-build/GIT.png)
* Run the following commands in the terminal emulator:

  ```
  git clone https://github.com/inkstitch/inkstitch
  git clone https://github.com/inkstitch/pyembroidery
  ```

## Edit Ink/Stitch requirements

* Open the new inkstitch folder in the file browser
* Open requirements.txt with your prefered text editor
  * Delete `./pyembroidery`
  * Replace `numpy<=1.17.4` with `numpy`

## Setup Python

* In the terminal emulator run the following commands:

  ```
  python -m pip install --upgrade pip
  python -m pip install wheel
  python -m pip install git+https://github.com/gtaylor/python-colormath
  python -m pip install -e pyembroidery/
  cd inkstitch
  python -m pip install -r requirements.txt
  python -m pip install pyinstaller
  ```
* For debugging with pydevd also run:
  ```
  python -m pip install pydevd
  ```

## Setup yarn

* In the terminal emulator run

  ```
  npm install --global yarn
  ```

## Set Ink/Stitch environment variables BUILD and VERSION

* In the file browser open the `Makefile` with your predered text editor
  Add these line to the Makefile at the beginging:

  ```
  export BUILD=windows
  export VERSION=my-dev-build
  ```

* Open the bin folder and edit the file `build-distribution-archives`

  Comment out VERSION

  ```
  # VERSION
  ```

* Also in the bin folder edit `build-windows-installer`

  Update VERSION to the **same** name which you used in the Makefile

  ```
  VERSION=my-dev-build
  ```

## Build Ink/Stitch

* In the terminal emulator run:

  ```
  make distclean && make dist
  ```

* In the file browser you will find the finished builds in the folder `artifacts`
