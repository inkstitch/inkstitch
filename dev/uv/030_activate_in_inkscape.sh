#!/usr/bin/env bash
# Activate the current Ink/Stitch worktree in Inkscape.
#
# What it does:
# - Resolves the current worktree root from the my_scripts symlink context.
# - Resolves the Inkscape user data directory: --config-dir, else the directory
#   reported by `inkscape --user-data-directory`, else the per-OS default.
# - Points <user data>/extensions/inkstitch-<postfix> to that worktree root.
#   On Windows the link is created through PowerShell: an NTFS symlink, and,
#   when that fails (no admin rights, no Developer Mode), a junction, which
#   needs neither; --symlink/--junction force one method (for testing). A full
#   copy of the worktree is never made.
# - Updates python-interpreter in <user data>/preferences.xml to the installed
#   uvr launcher (default, auto-detects the right python; on Windows the
#   console-free uvr-gui launcher is used) or, with --use-python, to the
#   worktree virtual environment's python.
# - Reports a system-wide Ink/Stitch installation (from a packaged install,
#   e.g. a distribution package) that Inkscape would load alongside the user
#   extension symlink, and offers to remove it interactively.
#
# Runs on Linux, macOS, and Windows (Git Bash/MSYS2/Cygwin).
set -euo pipefail

usage() {
    printf 'Usage: %s [-y|--yes] [-p|--postfix POSTFIX] [--use-uvr|--use-python]\n' "$0"
    printf '          [-i|--inkscape BIN] [-c|--config-dir DIR] [--symlink|--junction]\n'
    printf '%s\n' \
        '  -p, --postfix POSTFIX  Use extensions/inkstitch-POSTFIX (default: dev).' \
        '  -i, --inkscape BIN     Inkscape executable used to query the user data' \
        '                         directory (default: auto-detected).' \
        '  -c, --config-dir DIR   Inkscape user data directory; skips the query and' \
        '                         the per-OS fallback.' \
        '  -y, --yes              Do not ask before activating or removing links.' \
        '  --use-uvr              Set python-interpreter to the uvr launcher (default;' \
        '                         on Windows the console-free uvr-gui is used).' \
        '  --use-python           Set python-interpreter to the worktree venv python.' \
        '  --symlink              Windows: force an NTFS symlink (needs Developer' \
        '                         Mode or elevation); no junction fallback.' \
        '  --junction             Windows: force a junction (no admin rights, but' \
        '                         cannot target a network/UNC path).' \
        'Windows default (no switch): try a symlink first, then a junction, then' \
        'an elevated symlink (UAC), then print manual instructions.' \
        'A packaged, system-wide Ink/Stitch install is reported; removing it is' \
        'offered interactively only (never with -y).'
}

assume_yes=false
postfix=dev
use_uvr=true
inkscape_bin=''
config_dir_override=''
# auto: symlink, then junction, then elevated, then instructions (Windows).
link_method=auto
# Windows notes: the extension link is created through PowerShell; MSYS ln -s
# is not used because it would copy the worktree. A junction needs no admin
# rights; --symlink/--junction force the link type (useful for testing).
while (($#)); do
    case "$1" in
    -y | --yes)
        assume_yes=true
        ;;
    -p | --postfix)
        if (($# < 2)) || [[ -z "$2" ]]; then
            printf 'Error: %s requires a non-empty postfix.\n' "$1" >&2
            exit 2
        fi
        postfix=$2
        shift
        ;;
    -i | --inkscape)
        if (($# < 2)) || [[ -z "$2" ]]; then
            printf 'Error: %s requires an Inkscape executable.\n' "$1" >&2
            exit 2
        fi
        inkscape_bin=$2
        shift
        ;;
    --inkscape=*)
        inkscape_bin=${1#*=}
        if [[ -z "$inkscape_bin" ]]; then
            printf 'Error: %s requires an Inkscape executable.\n' "$1" >&2
            exit 2
        fi
        ;;
    -c | --config-dir)
        if (($# < 2)) || [[ -z "$2" ]]; then
            printf 'Error: %s requires a directory.\n' "$1" >&2
            exit 2
        fi
        config_dir_override=$2
        shift
        ;;
    --config-dir=*)
        config_dir_override=${1#*=}
        if [[ -z "$config_dir_override" ]]; then
            printf 'Error: %s requires a directory.\n' "$1" >&2
            exit 2
        fi
        ;;
    --use-uvr)
        use_uvr=true
        ;;
    --use-python)
        use_uvr=false
        ;;
    --symlink)
        link_method=symlink
        ;;
    --junction)
        link_method=junction
        ;;
    -h | --help)
        usage
        exit 0
        ;;
    *)
        usage >&2
        exit 2
        ;;
    esac
    shift
done

if [[ ! "$postfix" =~ ^[A-Za-z0-9._-]+$ ]]; then
    printf 'Error: postfix may contain only letters, digits, dots, underscores, and hyphens.\n' >&2
    exit 2
fi

if [[ -n "$inkscape_bin" ]] && ! command -v "$inkscape_bin" >/dev/null 2>&1; then
    printf 'Error: Inkscape executable not found: %s\n' "$inkscape_bin" >&2
    exit 1
fi

# ---------------------------------------------------------------------------
# Inkscape discovery (Linux, macOS, Windows via Git Bash/MSYS2/Cygwin)
# ---------------------------------------------------------------------------

case "$(uname -s 2>/dev/null || printf 'unknown')" in
Darwin) platform=macos ;;
*CYGWIN* | *MINGW* | *MSYS* | *Windows*) platform=windows ;;
*) platform=linux ;;
esac

# Turn a platform-native path (what Inkscape prints on Windows) into the POSIX
# form this script uses internally.
to_posix_path() {
    local path=$1
    if [[ "$platform" == windows ]]; then
        if command -v cygpath >/dev/null 2>&1; then
            cygpath -u "$path"
            return 0
        fi
        path=$(printf '%s' "$path" | tr '\\' '/')
        if [[ "$path" =~ ^([A-Za-z]):/(.*)$ ]]; then
            path="/$(printf '%s' "${BASH_REMATCH[1]}" | tr '[:upper:]' '[:lower:]')/${BASH_REMATCH[2]}"
        fi
    fi
    printf '%s' "$path"
}

# Turn a POSIX path into the platform-native form Inkscape expects.
to_native_path() {
    local path=$1
    if [[ "$platform" == windows ]] && command -v cygpath >/dev/null 2>&1; then
        cygpath -w "$path"
        return 0
    fi
    printf '%s' "$path"
}

# Escape a value used as the replacement of a sed s|...|...| command.
escape_sed_replacement() {
    printf '%s' "$1" | sed -e 's/[\\&|]/\\&/g'
}

# Inkscape executables to try, most likely first.
inkscape_candidates() {
    if [[ "$platform" == windows ]]; then
        # inkscape.com is the console wrapper; inkscape.exe cannot write to a pipe.
        printf '%s\n' inkscape.com inkscape.exe inkscape
        printf '%s\n' \
            '/c/Program Files/Inkscape/bin/inkscape.com' \
            '/c/Program Files (x86)/Inkscape/bin/inkscape.com' \
            '/c/Program Files/Inkscape/bin/inkscape.exe' \
            '/c/Program Files (x86)/Inkscape/bin/inkscape.exe'
    elif [[ "$platform" == macos ]]; then
        printf '%s\n' inkscape /Applications/Inkscape.app/Contents/MacOS/inkscape
    else
        printf '%s\n' inkscape
    fi
}

# Locate an Inkscape executable, or return non-zero when none is usable.
find_inkscape() {
    local candidate resolved
    while IFS= read -r candidate; do
        if [[ "$candidate" == */* ]]; then
            if [[ -x "$candidate" ]]; then
                printf '%s' "$candidate"
                return 0
            fi
        elif resolved=$(command -v "$candidate" 2>/dev/null); then
            printf '%s' "$resolved"
            return 0
        fi
    done < <(inkscape_candidates)
    return 1
}

# Inkscape user data directories to try, most likely first.
user_data_dir_candidates() {
    if [[ "$platform" == macos ]]; then
        printf '%s\n' \
            "$HOME/Library/Application Support/org.inkscape.Inkscape/config/inkscape" \
            "$HOME/.config/inkscape"
    elif [[ "$platform" == windows ]]; then
        printf '%s\n' "$(to_posix_path "${APPDATA:-$HOME/AppData/Roaming}")/inkscape"
        printf '%s\n' "$HOME/.config/inkscape"
    else
        printf '%s\n' "${XDG_CONFIG_HOME:-$HOME/.config}/inkscape"
    fi
}

# Resolve the Inkscape user data directory: --config-dir first, then the
# directory Inkscape reports, then the per-OS defaults.
resolve_user_data_dir() {
    local candidate reported fallback=''
    if [[ -n "$config_dir_override" ]]; then
        to_posix_path "$config_dir_override"
        return 0
    fi
    if [[ -n "$inkscape_bin" ]]; then
        reported=$("$inkscape_bin" --user-data-directory 2>/dev/null) || reported=''
        reported=$(to_posix_path "${reported%%$'\n'*}")
        if [[ "$reported" == /* ]]; then
            printf '%s' "$reported"
            return 0
        fi
    fi
    while IFS= read -r candidate; do
        [[ -n "$fallback" ]] || fallback=$candidate
        if [[ -f "$candidate/preferences.xml" ]]; then
            printf '%s' "$candidate"
            return 0
        fi
    done < <(user_data_dir_candidates)
    while IFS= read -r candidate; do
        if [[ -d "$candidate" ]]; then
            printf '%s' "$candidate"
            return 0
        fi
    done < <(user_data_dir_candidates)
    printf '%s' "$fallback"
}

# System data directory candidates, most likely first.
system_data_dir_candidates() {
    if [[ "$platform" == macos ]]; then
        printf '%s\n' \
            '/Applications/Inkscape.app/Contents/share/inkscape' \
            '/usr/local/share/inkscape'
    elif [[ "$platform" == windows ]]; then
        printf '%s\n' \
            '/c/Program Files/Inkscape/share/inkscape' \
            '/c/Program Files (x86)/Inkscape/share/inkscape'
    else
        printf '%s\n' '/usr/share/inkscape' '/usr/local/share/inkscape'
    fi
}

# Resolve the Inkscape system data directory: the directory Inkscape reports,
# then the install location guessed from the executable, then per-OS defaults.
resolve_system_data_dir() {
    local candidate reported install_root
    if [[ -n "$inkscape_bin" ]]; then
        reported=$("$inkscape_bin" --system-data-directory 2>/dev/null) || reported=''
        reported=$(to_posix_path "${reported%%$'\n'*}")
        if [[ "$reported" == /* && -d "$reported" ]]; then
            printf '%s' "$reported"
            return 0
        fi
    fi
    if [[ "$platform" == windows && "$inkscape_bin" == */bin/* ]]; then
        install_root=${inkscape_bin%/bin/*}
        if [[ -d "$install_root/share/inkscape" ]]; then
            printf '%s' "$install_root/share/inkscape"
            return 0
        fi
    fi
    while IFS= read -r candidate; do
        if [[ -d "$candidate" ]]; then
            printf '%s' "$candidate"
            return 0
        fi
    done < <(system_data_dir_candidates)
    printf '%s' "$(system_data_dir_candidates | head -n 1)"
}

# Ink/Stitch entries (from a packaged install) in the system extension
# directory. A case variant covers case-insensitive file systems.
list_system_inkstitch_entries() {
    [[ -d "$system_extensions_dir" ]] || return 0
    local entry
    for entry in "$system_extensions_dir"/inkstitch* "$system_extensions_dir"/Inkstitch*; do
        [[ -e "$entry" || -L "$entry" ]] || continue
        printf '%s\n' "${entry##*/}"
    done | sort -u
}

# List extension directory entries as "name -> target" for symlinks, "name"
# otherwise. A glob loop keeps this portable (BSD find has no -printf).
list_extension_entries() {
    local entry
    for entry in "$extensions_dir"/* "$extensions_dir"/.[!.]*; do
        [[ -L "$entry" || -e "$entry" ]] || continue
        if [[ -L "$entry" ]]; then
            printf '%s -> %s\n' "${entry##*/}" "$(readlink "$entry")"
        else
            printf '%s\n' "${entry##*/}"
        fi
    done | sort
}

# Names of the extension symlinks that can be removed.
list_extension_links() {
    local entry
    for entry in "$extensions_dir"/* "$extensions_dir"/.[!.]*; do
        [[ -L "$entry" ]] || continue
        printf '%s\n' "${entry##*/}"
    done | sort
}

# Escape a value for a single-quoted PowerShell string literal.
escape_powershell_single_quotes() {
    printf '%s' "$1" | sed "s/'/''/g"
}

# LinkType of a Windows path: SymbolicLink, Junction, or empty when the path
# is a plain file or directory (MSYS sees junctions as plain directories).
get_windows_link_type() {
    local path_native=$1
    powershell.exe -NoProfile -NonInteractive -Command \
        "\$t = (Get-Item -LiteralPath '$(escape_powershell_single_quotes "$path_native")' -Force -ErrorAction SilentlyContinue).LinkType; if (\$t) { \$t }" \
        2>/dev/null | tr -d '\r'
}

# Reparse target of a Windows symlink or junction, in the native spelling.
get_windows_link_target() {
    local path_native=$1
    powershell.exe -NoProfile -NonInteractive -Command \
        "(Get-Item -LiteralPath '$(escape_powershell_single_quotes "$path_native")' -Force -ErrorAction SilentlyContinue).Target" \
        2>/dev/null | tr -d '\r'
}

# Create a Windows link of the given type (SymbolicLink or Junction) through
# PowerShell. Non-zero on failure (-ErrorAction Stop makes errors terminating).
windows_new_link() {
    local item_type=$1 link_native=$2 target_native=$3
    powershell.exe -NoProfile -NonInteractive -Command \
        "New-Item -ItemType $item_type -Path '$(escape_powershell_single_quotes "$link_native")' -Target '$(escape_powershell_single_quotes "$target_native")' -ErrorAction Stop | Out-Null"
}

# True when the current Windows process runs elevated (as administrator).
windows_is_elevated() {
    powershell.exe -NoProfile -NonInteractive -Command \
        "([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)" \
        2>/dev/null | grep -qi true
}

# Target of an existing extension link for display; junctions need PowerShell
# because MSYS readlink cannot read them. Returns empty for a missing path.
get_link_target_display() {
    local link_path=$1
    if [[ "$platform" == windows && -e "$link_path" && ! -L "$link_path" ]]; then
        get_windows_link_target "$(to_native_path "$link_path")"
        return 0
    fi
    if [[ -L "$link_path" ]]; then
        readlink "$link_path"
    fi
    return 0
}

# Remove a symlink or junction; succeeds only when the path is gone.
remove_extension_entry() {
    local link_path=$1 link_type
    if [[ -L "$link_path" ]]; then
        rm "$link_path"
    elif [[ "$platform" == windows && -e "$link_path" ]] &&
        [[ "$(get_windows_link_type "$(to_native_path "$link_path")")" == Junction ]]; then
        # cmd rmdir removes a junction itself, never its contents.
        cmd //c rmdir "$(to_native_path "$link_path")" >/dev/null 2>&1 || return 1
    else
        return 1
    fi
    [[ ! -e "$link_path" && ! -L "$link_path" ]]
}

# Create the extension link. On Windows MSYS `ln -s` would silently copy the
# whole worktree (hundreds of MB, thousands of files) instead of linking, so
# links are created through PowerShell: an NTFS symlink, and, in the default
# (auto) mode, a junction when that fails; junctions need no admin rights.
create_extension_link() {
    local link_native target_native elevated_command created_type existing_type
    local esc_link esc_target replace_copy_answer link_created=false
    # A plain directory at the link path is a copied Ink/Stitch, never a
    # link; on every platform it must be replaced first, otherwise `ln -sfn`
    # would nest the new symlink inside the copy instead of replacing it.
    existing_type=''
    if [[ "$platform" == windows && -e "$inkstitch_link" ]]; then
        existing_type=$(get_windows_link_type "$(to_native_path "$inkstitch_link")")
    fi
    if [[ -e "$inkstitch_link" && ! -L "$inkstitch_link" && "$existing_type" != Junction ]]; then
        if [[ "$assume_yes" != true ]]; then
            printf 'Found a full copy instead of a link: %s\n' "$inkstitch_link"
            printf 'Replace the copy with a link? [y/N] '
            read -r replace_copy_answer
            [[ "$replace_copy_answer" =~ ^[Yy]$ ]] || {
                printf '%s\n' 'Activation cancelled: the copy was kept.' >&2
                exit 1
            }
        fi
        rm -rf "$inkstitch_link"
        printf 'Removed copied extension directory: %s\n' "$inkstitch_link"
    elif [[ -L "$inkstitch_link" || "$existing_type" == Junction ]]; then
        remove_extension_entry "$inkstitch_link"
    fi
    if [[ "$platform" != windows ]]; then
        ln -sfn "$repo_root" "$inkstitch_link"
        if [[ ! -L "$inkstitch_link" ]]; then
            printf 'Error: %s is not a symlink after creation.\n' "$inkstitch_link" >&2
            exit 1
        fi
        return 0
    fi
    if ! command -v powershell.exe >/dev/null 2>&1; then
        printf '%s\n' \
            'Error: powershell.exe not found; cannot create the link.' >&2
        exit 1
    fi
    link_native=$(to_native_path "$inkstitch_link")
    target_native=$(to_native_path "$repo_root")
    esc_link=$(escape_powershell_single_quotes "$link_native")
    esc_target=$(escape_powershell_single_quotes "$target_native")
    if [[ "$link_method" == auto || "$link_method" == symlink ]]; then
        if windows_new_link SymbolicLink "$link_native" "$target_native"; then
            printf '%s\n' 'Created NTFS symlink.'
            link_created=true
        elif [[ "$link_method" == symlink ]]; then
            printf '%s\n' \
                'Symlink creation failed (missing privilege).' \
                'Retrying once through an elevated PowerShell; please accept the UAC prompt.'
            if ! powershell.exe -NoProfile -NonInteractive -Command \
                "Start-Process powershell -Verb RunAs -Wait -ArgumentList '-NoProfile','-Command','$(escape_powershell_single_quotes "New-Item -ItemType SymbolicLink -Path \"$link_native\" -Target \"$target_native\" | Out-Null")'"; then
                printf '%s\n' \
                    "Error: could not create the symlink even with elevation: $inkstitch_link" >&2
                printf '%s\n' \
                    'Enable Windows Developer Mode (Settings > Privacy & security > For developers)' \
                    "or create the link manually in an elevated PowerShell:" \
                    "  New-Item -ItemType SymbolicLink -Path '$link_native' -Target '$target_native'" >&2
                exit 1
            fi
            link_created=true
        else
            printf '%s\n' 'Symlink creation failed; falling back to a junction (no admin rights required).'
        fi
    fi
    if [[ "$link_created" != true ]]; then
        if windows_new_link Junction "$link_native" "$target_native"; then
            printf '%s\n' 'Created junction (no admin rights required).'
        else
            printf '%s\n' \
                "Error: junction creation failed; junctions cannot target network (UNC) paths: $target_native" >&2
            printf '%s\n' \
                'Retry with --symlink, or create a symlink manually:' \
                "  New-Item -ItemType SymbolicLink -Path '$link_native' -Target '$target_native'" >&2
            exit 1
        fi
    fi
    created_type=$(get_windows_link_type "$link_native")
    if [[ "$created_type" != SymbolicLink && "$created_type" != Junction ]]; then
        printf 'Error: %s is not a link after creation.\n' "$inkstitch_link" >&2
        exit 1
    fi
    if [[ "$link_method" == symlink && "$created_type" != SymbolicLink ]]; then
        printf 'Error: %s is a %s, but a symlink was requested.\n' "$inkstitch_link" "$created_type" >&2
        exit 1
    fi
    if [[ "$link_method" == junction && "$created_type" != Junction ]]; then
        printf 'Error: %s is a %s, but a junction was requested.\n' "$inkstitch_link" "$created_type" >&2
        exit 1
    fi
}

script_dir=$(dirname "${BASH_SOURCE[0]}")

if [[ "$script_dir" == . ]]; then
    project_dir=$(dirname "$PWD")
else
    project_dir=$PWD
fi

if ! repo_root=$(git -C "$project_dir" rev-parse --show-toplevel 2>/dev/null); then
    printf '%s\n' \
        'Error: no Ink/Stitch worktree was found.' \
        'Run this script from the my_scripts symlink in an Ink/Stitch worktree.' >&2
    exit 1
fi

if [[ ! -f "$repo_root/inkstitch.py" ]]; then
    printf 'Error: expected %s/inkstitch.py, but it was not found.\n' "$repo_root" >&2
    exit 1
fi

if [[ -z "$inkscape_bin" ]]; then
    if ! inkscape_bin=$(find_inkscape); then
        inkscape_bin=''
    fi
fi

inkscape_config_dir=$(resolve_user_data_dir)
extensions_dir="$inkscape_config_dir/extensions"
inkstitch_link="$extensions_dir/inkstitch-$postfix"
preferences_file="$inkscape_config_dir/preferences.xml"

system_data_dir=$(resolve_system_data_dir)
system_extensions_dir="$system_data_dir/extensions"

if [[ "$use_uvr" == true ]]; then
    # On Windows, plain uvr is a console program: Inkscape launching it would
    # open a console window for every extension run; uvr-gui stays windowless.
    if [[ "$platform" == windows ]]; then
        if ! python_path=$(command -v uvr-gui); then
            printf '%s\n' \
                'Warning: the uvr-gui launcher was not found in PATH.' \
                'Falling back to the worktree virtual environment Python.' >&2
            use_uvr=false
        fi
    elif ! python_path=$(command -v uvr); then
        printf '%s\n' \
            'Warning: the uvr launcher was not found in PATH.' \
            'Falling back to the worktree virtual environment Python.' >&2
        use_uvr=false
    fi
fi

if [[ "$use_uvr" != true ]]; then
    if [[ "$platform" == windows && -e "$repo_root/.venv/Scripts/pythonw.exe" ]]; then
        python_path="$repo_root/.venv/Scripts/pythonw.exe"
    else
        python_path="$repo_root/.venv/bin/python"
    fi
fi

# Inkscape stores the interpreter exactly as its platform spells it.
python_interpreter_value=$(to_native_path "$python_path")

current_python_path='not configured'
if [[ -f "$preferences_file" ]]; then
    current_python_path=$(sed -nE 's/.*python-interpreter="([^"]*)".*/\1/p' "$preferences_file" | head -n 1)
    current_python_path=${current_python_path:-not configured}
fi

mkdir -p "$extensions_dir"
printf '%s\n' 'Inkscape configuration:'
printf '  %-16s %s\n' 'User data:' "$inkscape_config_dir"
if [[ -n "$inkscape_bin" ]]; then
    printf '  %-16s %s\n' 'Executable:' "$inkscape_bin"
else
    printf '  %-16s %s\n' 'Executable:' 'not found (using the default directory)'
fi
printf '  %-16s %s\n' 'Python:' "$current_python_path"
extension_entries=()
while IFS= read -r extension_entry; do
    extension_entries+=("$extension_entry")
done < <(list_extension_entries)
if ((${#extension_entries[@]})); then
    printf '  %-16s %s\n' 'Extensions:' "${extension_entries[0]}"
    for extension_entry in "${extension_entries[@]:1}"; do
        printf '  %-16s %s\n' '' "$extension_entry"
    done
else
    printf '  %-16s %s\n' 'Extensions:' 'none'
fi

printf '  %-16s %s\n' 'System data:' "$system_data_dir"
system_inkstitch_entries=()
while IFS= read -r system_inkstitch_entry; do
    system_inkstitch_entries+=("$system_inkstitch_entry")
done < <(list_system_inkstitch_entries)
if ((${#system_inkstitch_entries[@]})); then
    printf '  %-16s %s\n' 'System Ink/Stitch:' "${system_inkstitch_entries[0]}"
    for system_inkstitch_entry in "${system_inkstitch_entries[@]:1}"; do
        printf '  %-16s %s\n' '' "$system_inkstitch_entry"
    done
    printf '%s\n' \
        'Warning: Inkscape would load Ink/Stitch from here and from the user' \
        'extension directory at the same time (duplicate extensions).'
else
    printf '  %-16s %s\n' 'System Ink/Stitch:' 'none'
fi

link_is_current=false
link_is_current_target=$(get_link_target_display "$inkstitch_link")
if [[ -L "$inkstitch_link" && "$link_is_current_target" == "$repo_root" ]]; then
    link_is_current=true
elif [[ "$platform" == windows && -e "$inkstitch_link" && ! -L "$inkstitch_link" ]]; then
    # Junctions look like plain directories to MSYS; compare via PowerShell.
    if [[ "$(get_windows_link_type "$(to_native_path "$inkstitch_link")")" == Junction ]]; then
        link_is_current_target=$(get_windows_link_target "$(to_native_path "$inkstitch_link")")
        if [[ "$link_is_current_target" == "$(to_native_path "$repo_root")" ||
        "$link_is_current_target" == "$repo_root" ]]; then
            link_is_current=true
        fi
    fi
fi

python_is_current=false
if [[ "$current_python_path" == "$python_interpreter_value" ]]; then
    python_is_current=true
fi

if [[ "$assume_yes" != true ]]; then
    while true; do
        removable_links=()
        while IFS= read -r removable_link; do
            removable_links+=("$removable_link")
        done < <(list_extension_links)
        if ((${#removable_links[@]} == 0)); then
            break
        fi
        printf '\n'
        printf '%s\n' 'Removable extension links:'
        for index in "${!removable_links[@]}"; do
            link_name=${removable_links[index]}
            if [[ "$link_name" == "$(basename "$inkstitch_link")" ]]; then
                if [[ "$link_is_current" == true && "$python_is_current" == true ]]; then
                    printf '  %d: %s (will not change: symlink and Python are current)\n' \
                        "$((index + 1))" "$link_name"
                elif [[ "$link_is_current" == true ]]; then
                    printf '  %d: %s (symlink will not change; Python will be updated)\n' \
                        "$((index + 1))" "$link_name"
                else
                    printf '  %d: %s (symlink will be overwritten on activation)\n' \
                        "$((index + 1))" "$link_name"
                fi
            else
                printf '  %d: %s\n' "$((index + 1))" "$link_name"
            fi
        done
        printf '\n'
        printf 'Remove links (numbers separated by spaces, empty to keep all, q to quit)? '
        read -r -a selected_link_numbers
        if ((${#selected_link_numbers[@]} == 0)); then
            break
        fi
        for selected_number in "${selected_link_numbers[@]}"; do
            if [[ "$selected_number" == q ]]; then
                printf '%s\n' 'Activation cancelled.'
                exit 0
            fi
        done
        for selected_number in "${selected_link_numbers[@]}"; do
            if [[ ! "$selected_number" =~ ^[0-9]+$ ]] ||
                ((selected_number < 1 || selected_number > ${#removable_links[@]})); then
                printf 'Skipping %s: not a valid link number.\n' "$selected_number" >&2
                continue
            fi
            link_name=${removable_links[selected_number - 1]}
            link_path="$extensions_dir/$link_name"
            if [[ -L "$link_path" || ("$platform" == windows && -e "$link_path") ]]; then
                if remove_extension_entry "$link_path"; then
                    printf 'Removed extension link: %s\n' "$link_path"
                    if [[ "$link_path" == "$inkstitch_link" ]]; then
                        link_is_current=false
                    fi
                else
                    printf 'Could not remove extension link: %s\n' "$link_path" >&2
                fi
            fi
        done
    done
fi

# Removing files owned by a package install must stay an explicit, interactive
# decision, so this offer is never acted on with -y.
if ((${#system_inkstitch_entries[@]})) && [[ "$assume_yes" != true ]]; then
    printf 'Remove the system Ink/Stitch installation(s)? [y/N] '
    read -r remove_system_answer
    if [[ "$remove_system_answer" =~ ^[Yy]$ ]]; then
        for system_inkstitch_entry in "${system_inkstitch_entries[@]}"; do
            system_inkstitch_path="$system_extensions_dir/$system_inkstitch_entry"
            if rm -rf "$system_inkstitch_path" 2>/dev/null; then
                printf 'Removed system Ink/Stitch: %s\n' "$system_inkstitch_path"
            else
                printf '%s\n' \
                    "Could not remove $system_inkstitch_path (permission denied)." \
                    'Remove it manually, for example with sudo or an elevated shell:'
                printf '  sudo rm -rf "%s"\n' "$system_inkstitch_path"
            fi
        done
    else
        printf '%s\n' 'Kept the system Ink/Stitch installation; expect duplicate extension warnings.'
    fi
fi

if [[ "$link_is_current" == true && "$python_is_current" == true ]]; then
    printf '%s\n' 'No changes needed: the extension symlink and Python interpreter are already active.'
    exit 0
fi

printf '\n'
printf '%s\n' 'Changes to apply:'
printf '  %-16s %s -> %s\n' 'Extension:' "$inkstitch_link" "$repo_root"
printf '  %-16s %s\n' 'Python:' "$python_interpreter_value"
printf '  %-16s %s\n' 'Preferences:' "$preferences_file"

if [[ "$assume_yes" != true ]]; then
    printf '\n'
    printf 'Continue? [y/N] '
    read -r confirmation
    [[ "$confirmation" =~ ^[Yy]$ ]] || {
        printf '%s\n' 'No changes made.'
        exit 0
    }
fi

create_extension_link

if [[ ! -f "$preferences_file" ]]; then
    printf 'Error: preferences file not found: %s\n' "$preferences_file" >&2
    exit 1
fi

if ! grep -q 'python-interpreter="' "$preferences_file"; then
    printf 'Error: python-interpreter attribute was not found in %s\n' "$preferences_file" >&2
    exit 1
fi

escaped_python_interpreter=$(escape_sed_replacement "$python_interpreter_value")
tmp_file=$(mktemp "${preferences_file}.XXXXXX")
sed -E "s|python-interpreter=\"[^\"]*\"|python-interpreter=\"$escaped_python_interpreter\"|" \
    "$preferences_file" >"$tmp_file"
mv "$tmp_file" "$preferences_file"

printf '\n'
printf '%s\n' 'Activation complete:'
printf '  %-16s %s\n' 'Worktree:' "$repo_root"
printf '  %-16s %s -> %s\n' 'Extension:' "$inkstitch_link" "$repo_root"
printf '  %-16s %s\n' 'Python:' "$python_interpreter_value"
printf '  %-16s %s\n' 'Preferences:' "$preferences_file"
