---
title: "Manual Setup for Linux and macOS"
permalink: /developers/inkstitch/manual-setup/
last_modified_at: 2026-02-09
toc: true
after_footer_scripts:
  - /assets/js/copy_code.js
---
A manual setup will allow you to edit the code while running the extension.

## How to Install Ink/Stitch Manually

The required python version for working with Ink/Stitch is >=3.11.0.
We recommend using `pyenv` to manage your Python virtual environmentm but any other virtual environment manager should work (ex. `conda`, `uv` etc..)

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

### 5. Configure Inkscape Python Environment (Linux only)

By default, Inkscape will use your system's python interpreter. On modern linux distributions, the [PEP668](https://peps.python.org/pep-0668/) standard prevents you from installing python packages directly into the system python interpreter.
To work around this limitation, we need to tell Inkscape to use the python interpreter we installed in step 2:

* Open the file `preferences.xml`.<br>
  The location can be found under `Edit > Preferences > System > User preferences`
* Close Inkscape before editing the file.<br>
  Otherwise it will be overwritten when Inkscape closes.
* Search for the term `<group id="extensions" />` and update to the correct Python interpreter.

  **Example:** Use `<group id="extensions" python-interpreter="/usr/local/bin/python3" />` where `/usr/local/bin/python3` is the value returned by `which python3`.

For more information see [Inkscape documentation](https://inkscape.gitlab.io/extensions/documentation/authors/interpreters.html#selecting-a-specific-interpreter-version-via-preferences-file).

### 6. Run Inkscape.

Changes to the Python code take effect the next time the extension is run. Changes to the extension description files (`*.inx`) take effect the next time Inkscape is restarted.

