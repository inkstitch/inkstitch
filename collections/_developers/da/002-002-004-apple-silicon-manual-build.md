---
title: "Apple Silicon Manual Build"
permalink: /da/developers/inkstitch/apple-silicon-manual-build/
last_modified_at: 2022-03-30
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

## Rosetta

Although we are not building for Intel macs, we still need Rosetta 2. To install run:

```
softwareupdate —install—rosetta
```

## Install Ink/Stitch dependencies

Now we can install Ink/Stitch build dependencies:

```
brew install python@3.9 gtk+3 pkg-config gobject-introspection geos libffi gettext wxpython npm pygobject3
```

Use your favourite text editor to add the following line to `~/.zprofile`:

```
export PATH=“$(brew --prefix)/opt/python@3.9/libexec/bin:$PATH”
```

Restart the terminal emulator. 

Download Ink/Stitch and pyembroidery source from GitHub:

```
git clone https://github.com/inkstitch/inkstitch
git clone https://github.com/inkstitch/pyembroidery.git
```

Edit `requirements.txt` located in /inkstitch:

- delete the entry `./pyembrodery`
- replace `numpy<=1.17.4` with `numpy`. The specified version of numpy in requirements.txt will not build for m1 arm.

Install Ink/Stitch requirements with pip:

```
pip install git+https://github.com/gtaylor/python-colormath
pip install -r requirements.txt
pip install pyinstaller
```

Locate the pyembroidery folder created by git. To install pyembroidery run:

```
pip install -e pyembroidery/
```

## Electron

For electron we need yarn to be installed. Run:

```
npm install --global yarn
```

The `package.json` file must be prepared to build electron with M1 processors. **Remove package dependencies in package.json** in `inkstitch/electron` and run:

```
cd electron
yarn remove electron-compile
yarn remove electron-prebuilt-compile
```

Upgrade several dependency versions in package.json:

```
yarn upgrade electron@^11.2.0
yarn upgrade electron-debug@^3.0.0
yarn upgrade electron-devtools-installer@^3.2.0
```

Edit `package.json` with your favourite text editor. Find the mac section, replace `"target": "dir"` with:

```
"target": [
        {
            "target": "dir",
            "arch": [
                "arm64"
            ]
        }
        ],
```

## Prepare the build scripts

Now several build scripts need to be prepared.

Add the following to the top of the `Makefile`:

```
export BUILD=osx
export VERSION=dev-m1
```

In the folder `inkstitch/bin` edit `build-distribution-archives`.
- comment out the first line by adding `#` in front of VERSION
- find line 64 and replace `cp -a electron/build/mac dist/inkstitch.app/Contents/MacOS/electron`
  with:

  ```
  cp -a electron/build/mac-arm64 dist/inkstitch.app/Contents/MacOS/electron
  ```

## Build Ink/Stitch

Now Ink/Stitch is ready to be built.

In the inkstitch folder run:

```
make dist
```

When successful the Ink/Stitch installer package will be located in inkstitch/artifacts.

To rebuild run:

```
make distclean && make dist
```
