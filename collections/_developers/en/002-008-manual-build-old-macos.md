---
title: "Manual Build: Older macOS systems"
permalink: /developers/inkstitch/manual-build-old-macos/
last_modified_at: 2024-10-01
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
sudo port -v -b install gtk-devel libffi geos gettext gobject-introspection pkgconfig tcl curl sqlite3 readline
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

Install pip packages get inkstitch from github

```
git clone https://github.com/inkstitch/inkstitch
git clone https://github.com/inkstitch/pyembroidery.git
python -m pip install -r inkstitch/requirements.txt
python -m pip uninstall -y shapely
python -m pip cache remove shapely
python -m pip install -v shapely --no-binary shapely
python -m pip install pyinstaller
```

## Manual Install

From this point a manual install is possible. Check the [manual setup guide](/developers/inkstitch/manual-setup/) on the website. Continue from step 4.

## Build Ink/Stitch

Now Ink/Stitch is ready to be built.

In the inkstitch folder run:

```
make distlocal
```

When successful the Ink/Stitch installer package will be located in inkstitch/artifacts.

To clean inkstitch directory run:

```
make distclean

