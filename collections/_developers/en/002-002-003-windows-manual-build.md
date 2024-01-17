---
title: "Windows Manual Install and Manual Build"
permalink: /developers/inkstitch/windows-manual-build/
last_modified_at: 2024-01-17
toc: true
---
**Info:** For this description we use **`foo`** as a user name. Whenever it occures **replace it** with your personal windows user name.
{: .notice--warning }

## Requirements

Install these dependancies to build a local build of inkstitch for windows.

* [Python](https://www.python.org/downloads/release/python-398/)

  Depending on your target arch, select either 32bit or 64 bit version and run the installer.
  Check "Add Python x.xx to PATH".
  This for the bash enviroment to find python.
  ![Add python to path](/assets/images/developers/windows-manual-build/Python.png)
  Then click on "Install now"
* [Git for windows](https://gitforwindows.org/)

  This installs git as well as providing a terminal emulator to run build scripts.

  Download 
  Use the default settings during installation.
* [nodejs](https://nodejs.org/en/download/)

  Install LTS 32bit or 64bit version (depending on your target arch). Install with default settings.

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

## Enable long names for git

* In the search bar type `cdm` and chose `Run as administrator`.

  ![Run CMD as administrator](/assets/images/developers/windows-manual-build/cmd-admin.png)

* Run the following command

  ```
  git config --system core.longpaths true
  ```

* Close the command prompt, we do not need admin rights after this.

## Download Ink/Stitch

* If you already have an Ink/Stitch version installed [uninstall](/docs/install-windows/#uninstall-inkstitch)
  it first to avoid double menu entries in Inkscape.

* Go to `Edit > Preferences > System` and open your extensions folder.

  ![Inkscape extensions folder](/assets/images/docs/en/extensions-folder-location-win.jpg)

* Right click into the file browser and click on `Git Bash Here` to download Ink/Stitch into the extensions folder

  ![Right click menu](/assets/images/developers/windows-manual-build/GIT.png)
* Run the following commands in the terminal emulator:

  ```
  git clone https://github.com/inkstitch/inkstitch
  git clone https://github.com/inkstitch/pyembroidery
  ```

## Setup Python

* For **32bit** run the following commands in the terminal emulator:
  ```
  python -m pip install --upgrade pip
  python -m pip install wheel
  python -m pip install pillow==9.5.0
  python -m pip install numpy==1.23.1
  python -m pip install scipy==1.9.0
  pip install wxPython
  ```
* For **64bit** run the following commands in the terminal emulator:
  ```
  python -m pip install --upgrade pip
  python -m pip install wheel
  ```
* Now we are ready to install the rest of the requirements through the Ink/Stitch requirements file
  ```
  python -m pip install -r inkstitch/requirements.txt
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

## Manual Install for developing Ink/Stitch

* We prepared everything to finally setup Ink/Stitch itself. In your terminal emulator run:
  ```
  cd inkstitch
  make manual
  ```

* After adding a new template for new Ink/Stitch extensions, run the following command to update the Inskcape menu entries.
  ```
  make inx
  ```
  If you are running Ink/Stitch through Inkscape, close and reopen Inkscape after running the command.
* You can now use the Ink/Stitch installation. Changes to the Python code take effect the next time the extension is run.

## Generate a build to test run your update on other Windows systems

* To build Ink/Stitch you'll need to install pyinstaller.
  ```
  python -m pip install pyinstaller==5.13.2
  ```

* In the terminal emulator run:

  ```
  cd inkstitch
  make distlocal
  ```

* In the file browser you will find the finished builds in the folder `artifacts`
