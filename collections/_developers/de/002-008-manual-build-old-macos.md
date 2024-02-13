---
title: "Manual Build: Older macOS systems"
permalink: /de/developers/inkstitch/manual-build-old-macos/
last_modified_at: 2023-02-11
toc: true
---
This is an instructional guide how to build Ink/Stitch locally. The manual install for developers is described in the [manual setup section](/developers/inkstitch/manual-setup/).
{: .notice--info}

## Build requirements

* MacPorts 

  We recommend to use [macports](https://www.macports.org/) on older macOS systems. Set the -b flag to install prebuilt binary packages to speed things up.
* commnadline tools for mojave
* pyenv (see below)

Additionally in the build process you will need to install the following packages:

```
sudo port -v -b install gtk-devel libffi geos gettext gobject-introspection pkgconfig tcl curl sqlite3 readline nodejs16 yarn
```

### Install pyenv

Clone the pyenv repository

```
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
```

Build pyenv

```
cd ~/.pyenv && src/configure && make -C src
cd ..
```

Run these commands to make pyenv work in your terminal

```
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
```

```
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
echo 'eval "$(pyenv init -)"' >> ~/.bash_profile
```

For this to take effect run:

```
exec "$SHELL"
```

Build python:

```
env PYTHON_CONFIGURE_OPTS="--enable-framework" pyenv install -v 3.8.9
```

Set the version number

```
pyenv global 3.8.9
```

### Install Ink/Stitch requirements

Update the pip manager

```
python -m pip install -v —-upgrade pip
```

Install pip packages

```
python -m pip install -v wheel PyGObject pyinstaller 

python -m pip install -v https://files.pythonhosted.org/packages/31/9a/92b7be406a506177ab5ba079b67b7790f65b0d8e0091d0879978098f7d86/wxPython-4.1.1-cp38-cp38-macosx_10_9_x86_64.whl 
python -m pip install -v https://files.pythonhosted.org/packages/84/86/4f38fa30c112c3590954420f85d95b8cd23811ecc5cfc4bfd4d988d4db44/scipy-1.9.3-cp38-cp38-macosx_10_9_x86_64.whl

python -m pip install -v lxml==4.5.0 --no-binary lxml

python -m pip install -v Shapely==1.8.5 --no-binary Shapely
```

Install pyembroidery

```
git clone https://github.com/inkstitch/pyembroidery.git
python -m pip install -e pyembroidery/
```

Edit the requirements.txt to delete the pyembroidery entry then run

```
python -m pip install -v -r reqirements.txt
```

## Manual Install

From this point a manual install is possible. Check the [manual setup guide](/developers/inkstitch/manual-setup/) on the website. Continue from step 4.

## Build packages

In order to build and create a package the following must be done.

Open the Makefile in the inkstitch main folder and add the following entries to the begining of the file.

```
export BUILD=osx
export VERSION=localbuild
```

Then to `bin/build-distribution-archives` and comment out the first line with `#` and save.

From the inkstitch main folder run:

```
make dist
```

To rebuild run `make distclean` before rebuilding.

