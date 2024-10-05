---
title: "Manual Build: Apple Silicon"
permalink: /de/developers/inkstitch/apple-silicon-manual-build/
last_modified_at: 2024-09-30
toc: true
---
This is an instructional guide how to build Ink/Stitch locally. The manual install for developers is described in the [manual setup section](/developers/inkstitch/manual-setup/).
{: .notice--info}

## Homebrew

Ink/Stitch uses Homebrew to install the dependencies. Visit [https://brew.sh/](https://brew.sh/) and follow the instructions on the website to install. This will also install command line tools for Xcode.

Follow the final instructions of the Homebrew install, which configures Homebrew for your terminal by adding code to your `~/.zprofile`. It should look similar to this (update `foo` to your real user name):

```
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> /Users/foo/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

## Install Ink/Stitch dependencies

Now we can install Ink/Stitch build dependencies:

```
brew install python@3.9 gtk+3 pkg-config gobject-introspection geos libffi gettext pygobject3
```

Use your favourite text editor to add the following line to `~/.zprofile`:

```
export PATH=“$(brew --prefix)/opt/python@3.9/libexec/bin:$PATH”
```

Restart the terminal emulator. 

Download Ink/Stitch and pyembroidery source from GitHub and install pip packages:

```
git clone https://github.com/inkstitch/inkstitch
git clone https://github.com/inkstitch/pyembroidery.git
python -m pip install -v —-upgrade pip
python -m pip install -r inkstitch/requirements.txt
python -m pip uninstall -y shapely
python -m pip cache remove shapely
python -m pip install -v shapely --no-binary shapely
python -m pip install pyinstaller
```

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
```
