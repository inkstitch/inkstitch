#!/usr/bin/env bash
# Set up the project's uv environment on macOS, Linux,
# or Windows via Bash (Git Bash/WSL).
set -euo pipefail
# set -x

PYTHON_VERSION="3.13"
CLEAN_VENV=false
while [[ $# -gt 0 ]]; do
    case "$1" in
    -y | --yes)
        CLEAN_VENV=true
        shift
        ;;
    --py)
        PYTHON_VERSION="$2"
        shift 2
        ;;
    --py=*)
        PYTHON_VERSION="${1#*=}"
        shift
        ;;
    -h | --help)
        echo "Usage: $0 [-y|--yes] [--py <python-version>]" >&2
        exit 0
        ;;
    *)
        echo "Usage: $0 [-y|--yes] [--py <python-version>]" >&2
        echo "Unknown argument: $1" >&2
        exit 1
        ;;
    esac
done

script_dir=$(dirname "${BASH_SOURCE[0]}")

if [[ "$script_dir" == . ]]; then
    project_dir=$(dirname "$PWD")
else
    project_dir=$PWD
fi

if ! project_dir=$(git -C "$project_dir" rev-parse --show-toplevel 2>/dev/null); then
    echo 'Error: no Ink/Stitch worktree was found.' >&2
    echo 'Run this script from the my_scripts symlink in an Ink/Stitch worktree.' >&2
    exit 1
fi

# Platform detection: Linux distros may need the distro-specific wxPython
# find-links wheel, while macOS and Windows wheels come from PyPI. WSL reports
# "Linux" and has /etc/os-release, so it takes the Linux path.
case "$(uname -s 2>/dev/null || printf 'unknown')" in
Darwin) platform=macos ;;
*CYGWIN* | *MINGW* | *MSYS* | *Windows*) platform=windows ;;
Linux) platform=linux ;;
*) platform=unknown ;;
esac

os_name='unknown'
os_id=$platform
os_id_like='none'
os_version='unknown'
ubuntu_codename='none'
WXPYTHON_VERSION="${WXPYTHON_VERSION:-4.2.5}"
WXPYTHON_PLATFORM=''
SYNC_OPTIONS=()
if [[ "$platform" == linux ]]; then
    [[ -f /etc/os-release ]] || {
        echo 'Error: no /etc/os-release; cannot identify the Linux distribution.' >&2
        exit 1
    }
    # shellcheck disable=SC1091
    source /etc/os-release
    case "${ID:-}" in
    ubuntu) WXPYTHON_PLATFORM="ubuntu-${VERSION_ID}" ;;
    linuxmint)
        case "${UBUNTU_CODENAME:-}" in
        noble) WXPYTHON_PLATFORM=ubuntu-24.04 ;;
        jammy) WXPYTHON_PLATFORM=ubuntu-22.04 ;;
        focal) WXPYTHON_PLATFORM=ubuntu-20.04 ;;
        *) WXPYTHON_PLATFORM= ;;
        esac
        ;;
    centos | debian | fedora | rocky) WXPYTHON_PLATFORM="$ID-${VERSION_ID%%.*}" ;;
    *) WXPYTHON_PLATFORM= ;;
    esac
    [[ -n "$WXPYTHON_PLATFORM" ]] || {
        echo "Unsupported Linux distribution: ${ID:-unknown} ${VERSION_ID:-}" >&2
        exit 1
    }
    WXPYTHON_URL="https://extras.wxpython.org/wxPython4/extras/linux/gtk3/$WXPYTHON_PLATFORM"
    SYNC_OPTIONS=(--find-links "$WXPYTHON_URL")
    os_name="${PRETTY_NAME:-unknown}"
    os_id="${ID:-unknown}"
    os_id_like="${ID_LIKE:-none}"
    os_version="${VERSION_ID:-unknown}"
    ubuntu_codename="${UBUNTU_CODENAME:-${VERSION_CODENAME:-none}}"
elif [[ "$platform" == macos ]]; then
    os_version=$(sw_vers -productVersion 2>/dev/null || printf 'unknown')
    os_name="macOS $os_version"
elif [[ "$platform" == windows ]]; then
    os_name="Windows ($(uname -s), ${MSYSTEM:-no MSYSTEM})"
    os_version=$(uname -r 2>/dev/null || printf 'unknown')
else
    echo 'Warning: unknown platform; wxPython will be installed from PyPI.' >&2
fi

cd "$project_dir"
VENV_PATH="$PWD/.venv"
UV_PATH="$(command -v uv || true)"
[[ -n "$UV_PATH" ]] || {
    echo "uv is required" >&2
    exit 1
}

printf '\nDetected configuration:\n'
printf '  Platform:        %s\n' "$platform"
printf '  OS:              %s\n' "$os_name"
printf '  ID:              %s\n' "$os_id"
printf '  ID like:         %s\n' "$os_id_like"
printf '  OS version:      %s\n' "$os_version"
printf '  Ubuntu codename: %s\n' "$ubuntu_codename"
printf '  wxPython target: %s\n' "${WXPYTHON_PLATFORM:-PyPI}"
printf '  wxPython URL:    %s\n' "${WXPYTHON_URL:-PyPI}"
printf '  wxPython pin:    %s\n' "${WXPYTHON_URL:+$WXPYTHON_VERSION}"
printf '  Python:          %s\n' "$PYTHON_VERSION"
printf '  uv:              %s\n' "$UV_PATH"
printf '  Project:         %s\n' "$PWD"
printf '  Virtual env:     %s\n' "$VENV_PATH"
printf '  Clean .venv:     %s\n\n' "$CLEAN_VENV"

if [[ "$CLEAN_VENV" == true ]]; then
    echo "Removing virtual environment: $VENV_PATH"
    rm -rf "$VENV_PATH"
elif [[ -d "$VENV_PATH" ]]; then
    echo "Found virtual environment: $VENV_PATH"
    read -r -p "Set it up again? [y/N] " answer
    [[ "$answer" =~ ^[Yy]$ ]] || exit 0
else
    echo "Virtual environment will be created at: $VENV_PATH"
    read -r -p "Set up uv environment? [Y/n] " answer
    [[ "$answer" =~ ^[Nn]$ ]] && exit 0
fi

uv python pin "$PYTHON_VERSION"

if [[ -n "${WXPYTHON_URL:-}" ]]; then
    # pyproject.toml only pins "wxPython>=4.1.1", but the distro find-links
    # page may list several wheel versions; letting uv sync resolve against it
    # directly can fail, so pin and install wxPython explicitly first, then
    # relock so uv sees the installed version before syncing the rest.
    uv venv
    uv pip install -f "$WXPYTHON_URL" "wxPython==$WXPYTHON_VERSION"
fi

# Locale .mo files are force-included by the wheel build; ensure they exist
# before uv tries to build the editable package during lock/sync.
bash bin/generate-translation-files
bash bin/generate-version-file

uv lock "${SYNC_OPTIONS[@]}" --exclude-newer-package wxpython=2025-12-01
uv sync "${SYNC_OPTIONS[@]}"

if ! uv run python -c "import pyinstrument" 2>/dev/null; then
    uv pip install pyinstrument
fi

make inx
