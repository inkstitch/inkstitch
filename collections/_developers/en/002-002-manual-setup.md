---
title: "Manual Setup"
permalink: /developers/inkstitch/manual-setup/
last_modified_at: 2018-10-10
toc: false
---
A manual setup will allow you to edit the code while running the extension.

1. Clone the extension source and update submodule pyembroidery

   ```
   git clone https://github.com/inkstitch/inkstitch
   cd inkstitch
   git submodule init
   git submodule update
   ```
2. Python Dependencies

    A few python modules are needed. In some cases this extension uses features that aren’t available in the versions of the modules pre-packaged in distributions, so we recommend installing them directly with pip:
    ```
    pip install -r requirements.txt
    ```

    **Info:** You might need to remove wxPython and [install](https://wiki.wxpython.org/How%20to%20install%20wxPython) a platform specific package (e.g. Debian uses `python-wxgtk3.0`).
    {: .notice--info }

3. Prepare INX files

    ```
    for po in translations/*.po; do lang=${po%.*}; lang=${lang#*_}; mkdir -p locales/$lang/LC_MESSAGES; msgfmt $po -o locales/$lang/LC_MESSAGES/inkstitch.mo; done;
    mkdir inx
    bin/generate-inx-files
    ```

4. Symbolically link into the Inkscape extensions directory

    ```
    cd ~/.config/inkscape/extensions
    ln -s /path/to/inkstitch
    for i in inkstitch/inx/inkstitch_*.inx; do ln -s $i; done
    ln -s inkstitch/inkstitch.py
    ```

5. Run Inkscape.


**Info:** Changes to the Python code take effect the next time the extension is run. Changes to the extension description files (*.inx) take effect the next time Inkscape is restarted.
{: .notice--info }
