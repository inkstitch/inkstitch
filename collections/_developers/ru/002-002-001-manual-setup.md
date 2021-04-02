---
title: "Manual Setup"
permalink: /ru/developers/inkstitch/manual-setup/
last_modified_at: 2021-03-04
toc: true
---
A manual setup will allow you to edit the code while running the extension.

If you are aiming to debug extensions, and are running on Windows, some supplementary instructions are available at [windows-manual-setup](/developers/inkstitch/windows-manual-setup/)

## How to Install Ink/Stich Manually

### 1. Clone the extension source

```
git clone https://github.com/inkstitch/inkstitch
```

### 2. Install Pyembroidery

```
git clone https://github.com/inkstitch/pyembroidery.git
pip install -e pyembroidery/
```

We recommend to use `pyenv` to avoid the need of root privileges for `pip`.

### 3. Python Dependencies

A few python more modules are needed.
In some cases this extension uses features that aren’t available in the versions of the modules pre-packaged in distributions, so we recommend installing them directly with pip:

```
cd inkstitch
pip install -r requirements.txt
```

**Info:** You might need to remove wxPython and [install](https://wiki.wxpython.org/How%20to%20install%20wxPython) a platform specific package:<br />
   ⚫ Debian uses `python-wxgtk3.0`<br />
   ⚫ Ubuntu 16.04: `pip install -U -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-16.04 wxPython`
{: .notice--info }

### 4. Install Electron dependencies

The Ink/Stitch GUI uses Electron.  You'll need a working NodeJS installation of version 10 or greater.  If you don't have the `yarn` command, install it with `npm install yarn`.

Install Electron and its dependencies:

```
cd electron
yarn install
cd ..
```

### 5. Prepare INX files

```
make inx
```

This will create `*.inx` files for each locale in `inx/<locale>`.

Navigate to the newly created inx folder and delete all languages except for one or type

```
find inx/ -mindepth 1 -maxdepth 1 -type d -not -name en_US -exec rm -rf {} +
```

Substitute `en_US` with your preferred language (if exists).

The language chosen here will only have an effect on the Inkscape menu. Ink/Stitch dialogs use the system language.

### 6. Symbolically link into the Inkscape extensions directory

```
cd ~/.config/inkscape/extensions
ln -s /path/to/inkstitch
```

### 7. Run Inkscape.

Changes to the Python code take effect the next time the extension is run. Changes to the extension description files (`*.inx`) take effect the next time Inkscape is restarted.

## Troubleshoot

### ImportError: No module named shapely

If Ink/Stitch returns `ImportError: No module named shapely`, then it is likely the version of Python used by Inkscape and the version you installed the Python dependencies for above are different.

* Open the file `preferences.xml`.<br>
  The location can be found under `Edit > Preferences > System > User preferences`
* Close Inkscape before editing the file.<br>
  It will otherwise be overwritten when Inkscape closes.
* Search for the term `<group id="extensions" />` and update to the correct Python interpreter.

  **Example:** Use `<group id="extensions" python-interpreter="/usr/local/bin/python3" />` where `/usr/local/bin/python3` is the value returned by `which python3`.
