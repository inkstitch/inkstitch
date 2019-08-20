---
title: "Manual Setup"
permalink: /developers/inkstitch/manual-setup/
last_modified_at: 2019-05-01
toc: false
---
A manual setup will allow you to edit the code while running the extension. If you are aiming to debug extensions, and are running on Windows,
some supplementary instructions are available at [windows-manual-setup](/developers/windows-manual-setup/)  

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
    pip2 install -r requirements.txt
    ```

    **Info:** You might need to remove wxPython and [install](https://wiki.wxpython.org/How%20to%20install%20wxPython) a platform specific package:<br />
       ⚫ Debian uses `python-wxgtk3.0`<br />
       ⚫ Ubuntu 16.04: `pip install -U -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-16.04 wxPython`
    {: .notice--info }
    
    **Info:** If you only have Python 2 installed you may be able to use `pip` instead of `pip2`.
    {: .notice--info }

3. Install Electron dependencies
    The Ink/Stitch GUI uses Electron.  You'll need a working NodeJS installation of version 10 or greater.  If you don't have the `yarn` command, install it with `npm install yarn`.

    Install Electron and its dependencies:

    ```
    cd electron
    yarn install
    ```

4. Prepare INX files

    ```
    make inx
    ```

    This will create `*.inx` files for each locale in `inx/<locale>`.

5. Symbolically link into the Inkscape extensions directory

    ```
    cd ~/.config/inkscape/extensions
    ln -s /path/to/inkstitch
    for i in inkstitch/inx/en_US/inkstitch_*.inx; do ln -s $i; done
    ln -s inkstitch/inkstitch.py
    ```

    To use another language for Ink/Stitch menus inside Inkscape substitute `en_US` for another locale in `inx/`. Ink/Stich dialogs outside Inkscape use the OS language.

6. Run Inkscape.

    **Info:** If Ink/Stitch returns `ImportError: No module named shapely`, then it is likely the version of Python used by Inkscape and the version you installed the Python dependencies for above are different. Configure the Inkscape Python executable by editing `preferences.xml`. The location of `preferences.xml` can be found in Inkscape under Edit > Preferences > System > User extensions. You must *close Inkscape before editing this file*, it is over-written when Inkscape closes.<br/><br/>
    In `preferences.xml` update `<group id="extensions" />` to include the correct Python interpreter. For example,<br/><br/>
    `<group id="extensions" python-interpreter="/usr/local/bin/python2" />`<br/><br/>
    where, `/usr/local/bin/python2` is the value returned by `which python2`.
    {: .notice--info }


**Info:** Changes to the Python code take effect the next time the extension is run. Changes to the extension description files (`*.inx`) take effect the next time Inkscape is restarted.
{: .notice--info }
