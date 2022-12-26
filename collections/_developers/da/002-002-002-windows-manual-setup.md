---
title: "Windows Manual Setup"
permalink: /da/developers/inkstitch/windows-manual-setup/
last_modified_at: 2019-08-16
toc: false
---
This describes the manual setup for those who want to debug Ink/Stitch extensions on Windows.
A generic and more complete description for such debug environments is given on [manual-setup](/developers/inkstitch/manual-setup/).
This description focus only on the python part for the Windows environment.
The setup described will allow you to debug the code while running the extension, then edit in and run the extension again.

#### 1. You will need a Python environment (2.7 recommended).

Inkscape, which is the base application within which Ink/Stitch runs, does install a Python environment.
That environment does not contain all parts needed for Ink/Stitch extensions.
Using it as base to create a virtual environment on Windows is currently (inkscape 0.92.4) not a simple solution.
Easier than getting the Windows environment to use the one from inkscape, is to install a new Python and make a virtual environment from it.

In same way, extending the existing python packaged with inkscape, is giving some issues why this is the suggested method.

The python you are suggested to use is python 2.7. If you do not already have it installed, download and install it.
When it is installed, check your environment path variable. When the virtual environment runs,
the path variable is nbo longer important. Until you are there, the easiest plan is to see to that the python 2.7 paths (exe, lib, DLL) are first in the path.

#### 2. You will possibly want a git client
A git client is needed if you want to participate on github.
In that case, download a git client, and clone the inkstitch main directory.
A possible location would be c:\inkstitch, which is the directory used in the examples.
However, no Windows specific description of neither how to get a client or how to install the clone is given.
An easy way is to use PyCharm

#### 3. You need to create a virtual Python 2.7 environment for Ink/Stitch
This is the key. This environment will be used by inkscape when running extensions.
Again, no Windows specific description of how to download and set up this virtual environment is given.
Again, an easy way is to use PyCharm, and use the "requirements.txt" file which comes with Ink/Stitch

#### 4. Special actions needed for the virtual Python environment
The requirements.txt file which comes with Ink/Stitch does nto tell the whole story. There are a number of things left to do.
In Linux, more tools exist in the environment than is standard in Windows.
Normally you do not compile modules in Windows, which creates some specific issues for certain packages.
To solve them, we reside to downloading readymade wheel files (".whl" files). Files which can be installed by python, but come readymade for a specific environment.
For Windows 64, running a Python 64 bit, download below (later versions may exist, so use them, however, "cp27" and "amd64" is the name to look for:

    libxml2_python-2.9.3-cp27-none-win_amd64.whl
    lxml-4.4.1-cp27-cp27m-win_amd64.whl

Install the lixxml2 wheel file, into the virtual environment, any way you are used to. After that install the lxml file.
The lxml file require a specific way to install. This is due to the need to ensure it does not collide with libxml2 which it uses.
The pip command has to be the pip for the virtual environment, thus the assumption is that you issue the command from the command line,
with the working directory being the directory where that pip command resides.

    SET STATIC_DEPS=true
    .\pip install lxml-4.4.1-cp27-cp27m-win_amd64.whl
    set STATIC_DEPS=

You cannot install wx, instead install wxPython in normal way. To be on the safe side, install scour as well.

#### 5. shapely is a special difficulty
If you do not have OSGeo4W64 installed, you need to install it. Shapely requires two DLLs which come from that program (geos_c.dll and geos.dll).
After you have installed it, with the right path declarations, it will work. However, OSGeo4W64 may interfere with other programs (like illustrator).
Thus, a solution can be to copy those two file into a suitable path within your virtual environment. 
If you aim to use pyinstaller, that location need to be D:\Temp\BoxIssue\inkstitch-master\Lib\site-packages\shapely\DLLs.

With the DLLs in place, you can install shapely.

#### 6. To be able to execute Ink/Stitch from the virtual environment, you need to set PYTHONPATH
Ink/Stitch contain a submodule, pyembroidery, whose location is not automatically picked up. you thus need to declare it.
This is done by setting PYTHONPATH to the path where pyembroidery is placed. The top directory of pyembroidery.
Without using the "" ampersands around the path even if it contains spaces. Unusual in Windows environments.
If you want more directories in the path, for example inkstitch, add a semicolon and that path. I do not use it like that, but it should work.

    SET PYTHONPATH=D:\Path\To\pyembroidery

#### 7. Avoiding to have to run Ink/Stitch make files
In theory, you could now prepare inx-files using make. Instead download and install the latest Ink/Stitch release.
It will install all inx-files and locale files needed.
When done, copy your whole Ink/Stitch clone to where the inkstitch extension is.
In such a way that inkstitch.py from your clone overwrites inkstitch.py in the extension directory.
This means that when inkscape runs and Ink/Stitch extension, it will start your inkstitch.py file.

It also means whenever you change the code, you need to copy those code changes there.

#### 8. Set up inkscape to run your virtual Python:
This is done by going to the inkscape preferences file (preferences.xml) which is in your Roaming directory (C:\Users\xxxxxx\AppData\Roaming\inkscape).
xxxxxx is in this case your Windows user name. Exit incscape, and edit the file. 
Look for a group with id="extensions", and directly beneath add your python path, explicitly stating the python.exe file:

     id="extensions"
     python-interpreter="d:/path/to/virtualenv/Scripts/python.exe"
     
Whenever inkscape is now running an extension, it will use your python virtual environment.
If your inkscape installation is too old, it may get problems with your newere python environment. Then download and update inkscape.

#### 9. Tell Ink/Stitch to activate remote debugging
pydev is the suggested debugger to use. Again, no instruction is given here on how to install it. It is activated any time an Ink/Stitch extension is run assuming that you have a file named "DEBUG" in the same directory as the Ink/Stitch extension is installed for incscape. 
Thus goto the inkscape extension directory, and create the file (or a folder) named "DEBUG" in same directory as inkstitch.py

#### 10. Debugging now requires running a remote debugger
Start your remote debugger. Listen to port 5678. Start inkscape, from a place where the PYTHONPATH you set is active.
The way I do it is from the command line. From inside inkscape, call the Ink/Stitch exntesion you want to debug.
Ink/Stitch will call the debugger.

Any errors you may see before that is coming from inkscape, and then the import chain called by Ink/Stitch.
Install whatever modules are claimed as missing. 
If something is still amiss, best way to debug until the remote debugger starts is likely to go to inkscapes directory where inkex.py is, and edit that file.

    C.\Program Files\inkscape\share\extensions\inkex.py
