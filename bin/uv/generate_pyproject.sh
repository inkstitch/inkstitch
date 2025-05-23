#!/usr/bin/env bash

# - assuming pkg-config is installed
# - copy pyprojetc-in.toml to pyproject.toml
# - set the packages in pyproject.toml

set -e

function detect_platform() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        PLATFORM="linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        PLATFORM="darwin"
    elif [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        PLATFORM="windows"
    else
        PLATFORM="unknown"
    fi
}

# Detect the Linux distribution and version: as needed for wxPython
# see https://extras.wxpython.org/wxPython4/extras/linux/gtk3/
function detect_distro() {
    DISTRO_ID=""
    DISTRO_VER=""

    if [[ -f /etc/os-release ]]; then
        source /etc/os-release

        # Ubuntu and similar (Mint, Pop, Elementary, Zorin, atd.)
        if [[ "$ID" != "ubuntu" && "$ID_LIKE" == *"ubuntu"* && -n "$UBUNTU_CODENAME" ]]; then
            case "$UBUNTU_CODENAME" in
                jammy)  DISTRO_ID="ubuntu"; DISTRO_VER="22.04" ;;
                focal)  DISTRO_ID="ubuntu"; DISTRO_VER="20.04" ;;
                bionic) DISTRO_ID="ubuntu"; DISTRO_VER="18.04" ;;
                noble)  DISTRO_ID="ubuntu"; DISTRO_VER="24.04" ;;
                *)      DISTRO_ID="ubuntu"; DISTRO_VER="unknown" ;;
            esac

        # Fedora, CentOS, RHEL atd.
        elif [[ "$ID_LIKE" == *"rhel"* || "$ID" == "fedora" ]]; then
            DISTRO_ID="fedora"
            DISTRO_VER="$VERSION_ID"

        # Arch-based
        elif [[ "$ID_LIKE" == *"arch"* || "$ID" == "arch" ]]; then
            DISTRO_ID="arch"
            DISTRO_VER="rolling"

        # Debian and similar
        elif [[ "$ID_LIKE" == *"debian"* ]]; then
            DISTRO_ID="debian"
            DISTRO_VER="$VERSION_ID"

        # Ubuntu native
        elif [[ "$ID" == "ubuntu" ]]; then
            DISTRO_ID="ubuntu"
            DISTRO_VER="$VERSION_ID"

        # Fallback
        else
            DISTRO_ID="$ID"
            DISTRO_VER="$VERSION_ID"
        fi
    else
        DISTRO_ID="unknown"
        DISTRO_VER="unknown"
    fi
}

# detect python version from file .python-version
function detect_python_version() {
    if [[ -f ".python-version" ]]; then
        PYVER=$(cat .python-version)
    else
        echo "❌ file .python-version not found"
        exit 1
    fi

    # set the python version for the virtual environment
    PYVERNODOT="${PYVER//./}"
}


# for linux, we need to detect the pkg-config or pkgconf
function detect_pkgconf() {
    if command -v pkg-config &>/dev/null; then
        PKGCONF="pkg-config"
    elif command -v pkgconf &>/dev/null; then
        PKGCONF="pkgconf"
    else
        PKGCONF=""
        echo "❌ Neither pkg-config nor pkgconf found in PATH"
        exit 1
    fi
}



# for linux: detect gir 1.0 or 2.0 with pkg-config
function detect_gir() {
    if $PKGCONF --exists "gobject-introspection-1.0"  ; then
        PYGOBJECT="pygobject<=3.50"
        # echo "✅ gobject-introspection-1.0 found using pygobject<=3.50"
    elif $PKGCONF --exists "gobject-introspection-2.0" ; then
        PYGOBJECT="pygobject>3.50"
        # echo "✅ gobject-introspection-2.0 found"
    else
        echo "❌ gobject-introspection not found, install libgirepositoryX.X-dev"
        exit 1
    fi
}

function auto_detection() {
    echo "🔍 auto detection"
    detect_platform  # set $PLATFORM: linux, darwin, windows

    PYGOBJECT="pygobject"
    WXPYTHON="wxpython"


    if [[ "$PLATFORM" == "linux" ]]; then
        detect_pkgconf   # set $PKGCONF: pkg-config or pkgconf
        detect_distro    # set $DISTRO_ID, $DISTRO_VER: ubuntu, debian, arch, fedora, etc.
        # echo "Distro: $DISTRO_ID    Version: $DISTRO_VER"
        detect_python_version  # set $PYVER, $PYVERNODOT: python version, python version no dot
        # echo "Python version: $PYVER ($PYVERNODOT)"

        ### PyGObject
        detect_gir       # set $PYGOBJECT: pygobject<=3.50 or pygobject>3.50

        ### wxPython
        #      "https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-22.04/wxpython-4.2.3-cp39-cp39-linux_x86_64.whl"
        WXPYTHON="wxpython \@ https://extras.wxpython.org/wxPython4/extras/linux/gtk3/${DISTRO_ID}-${DISTRO_VER}"
        WXPYTHON="$WXPYTHON/wxpython-4.2.3-cp${PYVERNODOT}-cp${PYVERNODOT}-linux_x86_64.whl"

    fi

    PKG_EXTRA="    \"$PYGOBJECT\",\n    \"$WXPYTHON\","
}


PKG_EXTRA=""

# skip auto detection if --no-auto-detect is passed or -n is passed
for arg in "$@"; do
    if [[ "$arg" == "--no-auto-detect" || "$arg" == "-n" ]]; then
        echo "❌ auto detection skipped"
        no_auto_detection=1
        break
    fi
done


if [[ -z "$no_auto_detection" ]]; then
    auto_detection
fi


sed "s|{{PKG_EXTRA}}|$PKG_EXTRA|g" pyproject-in.toml > pyproject.toml

# sed -e "s|{{PYGOBJECT}}|$PYGOBJECT|g" \
#     -e "s|{{WXPYTHON}}|$WXPYTHON|g" \
#     pyproject-in.toml > pyproject.toml
