---
title: "Manual Setup for Linux and macOS"
permalink: /developers/inkstitch/manual-setup/
last_modified_at: 2025-10-19
toc: true
after_footer_scripts:
  - /assets/js/copy_code.js
---
A manual setup will allow you to edit the code while running the extension.

## How to Install Ink/Stitch Manually

We recommend using `pyenv` with python 3.8.

### 1. Clone the extension source

```
git clone https://github.com/inkstitch/inkstitch
```

### 2. Python Dependencies

A few more Python modules are needed.
In some cases this extension uses features that aren’t available in the versions of the modules pre-packaged in distributions, so we recommend installing them directly with pip.

```
python -m pip install -r inkstitch/requirements.txt
```

### 3. Prepare INX files

Now we need to create the files for the Inkscape menu:

```
cd inkstitch
make manual
```

When you later add or change a template file for Ink/Stitch extensions, simply run:

```
make inx
```

### 4. Symbolically link into the Inkscape extensions directory

```
cd ~/.config/inkscape/extensions
ln -s /path/to/inkstitch
```

### 5. Run Inkscape.

Changes to the Python code take effect the next time the extension is run. Changes to the extension description files (`*.inx`) take effect the next time Inkscape is restarted.

## Troubleshoot

### ImportError: No module named shapely

If Ink/Stitch returns `ImportError: No module named shapely`, then it is likely the version of Python used by Inkscape and the version you installed the Python dependencies for above are different.

* Open the file `preferences.xml`.<br>
  The location can be found under `Edit > Preferences > System > User preferences`
* Close Inkscape before editing the file.<br>
  Otherwise it will be overwritten when Inkscape closes.
* Search for the term `<group id="extensions" />` and update to the correct Python interpreter.

  **Example:** Use `<group id="extensions" python-interpreter="/usr/local/bin/python3" />` where `/usr/local/bin/python3` is the value returned by `which python3`.
