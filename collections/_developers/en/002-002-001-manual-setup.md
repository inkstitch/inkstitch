---
title: "Manual Setup"
permalink: /developers/inkstitch/manual-setup/
last_modified_at: 2021-10-14
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

We recommend to use `pyenv` with python 3.8.

### 3. Python Dependencies

A few python more modules are needed.
In some cases this extension uses features that aren’t available in the versions of the modules pre-packaged in distributions, so we recommend installing them directly with pip.

Since we already installed pyembroidery just temporarely comment it out before you run these commands.

```
cd inkstitch
pip install -r requirements.txt
```

### 4. Install Electron dependencies

The Ink/Stitch GUI uses Electron.  You'll need a working NodeJS installation of version 10 or greater.  If you don't have the `yarn` command, install it with `npm install yarn`.

Install Electron and its dependencies:

```
cd electron
yarn install
cd ..
```

### 5. Prepare INX files

Now we need to create the files for the Inkscape menu.

```
make inx
```

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
