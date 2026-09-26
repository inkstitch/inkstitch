#!/usr/bin/env bash
# Remove generated Python, test, lint, and packaging files.
set -euo pipefail

usage() {
    printf 'Usage: %s [--uv-venv|--uv] [-y|--yes]\n' "$0"
    printf '  Interactive by default: lists the targets and asks for 1, 2, or q.\n'
    printf '  [1] Generated artifacts outside .venv.\n'
    printf '  [2] Option 1 plus .venv, uv.lock, and .python-version.\n'
    printf '  --uv-venv, --uv  Add the uv targets to what -y removes (1 + 2).\n'
    printf '  -y, --yes        Skip the prompt and remove the selected targets.\n'
}

ASSUME_YES=false
INCLUDE_UV_VENV=false
for argument in "$@"; do
    case "$argument" in
    -y | --yes) ASSUME_YES=true ;;
    --uv-venv | --uv) INCLUDE_UV_VENV=true ;;
    -h | --help)
        usage
        exit 0
        ;;
    *)
        usage >&2
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

if ! PROJECT_ROOT=$(git -C "$project_dir" rev-parse --show-toplevel 2>/dev/null); then
    printf '%s\n' \
        'Error: no Ink/Stitch worktree was found.' \
        'Run this script from the my_scripts symlink in an Ink/Stitch worktree.' >&2
    exit 1
fi

# Option 1: generated artifacts outside .venv.
declare -a ARTIFACT_TARGETS=()
while IFS= read -r -d '' target; do
    ARTIFACT_TARGETS+=("$target")
done < <(
    find "$PROJECT_ROOT" \
        -path "$PROJECT_ROOT/.git" -prune -o \
        -path "$PROJECT_ROOT/.venv" -prune -o \
        -type d \( \
        -name '__pycache__' -o \
        -name '.pytest_cache' -o \
        -name '.mypy_cache' -o \
        -name '.ruff_cache' -o \
        -name '.tox' -o \
        -name '.nox' -o \
        -name 'build' -o \
        -name 'dist' -o \
        -name '*.egg-info' \
        \) -print0 -prune -o \
        -type f \( \
        -name '*.pyc' -o \
        -name '*.pyo' -o \
        -name '.coverage' \
        \) -print0
)

# Option 2: the uv environment, removed on top of option 1.
declare -a UV_TARGETS=()
for uv_path in .venv uv.lock .python-version; do
    if [[ -e "$PROJECT_ROOT/$uv_path" ]]; then
        UV_TARGETS+=("$PROJECT_ROOT/$uv_path")
    fi
done

# Print paths relative to the project root, or "(none)" for an empty list.
print_targets() {
    if (($# == 0)); then
        printf '    (none)\n'
        return 0
    fi
    local target
    for target in "$@"; do
        printf '    %s\n' "${target#"$PROJECT_ROOT"/}"
    done
}

printf '\nCleanup plan for: %s\n' "$PROJECT_ROOT"
printf '  [1] Generated artifacts outside .venv (%d path(s)):\n' "${#ARTIFACT_TARGETS[@]}"
# The "${array[@]+...}" form keeps an empty array valid under "set -u".
print_targets ${ARTIFACT_TARGETS[@]+"${ARTIFACT_TARGETS[@]}"}
printf '  [2] UV targets, removed together with [1] (%d path(s)):\n' "${#UV_TARGETS[@]}"
print_targets ${UV_TARGETS[@]+"${UV_TARGETS[@]}"}

# 1 = artifacts only, 2 = artifacts plus the uv targets.
choice=1
if [[ "$ASSUME_YES" != true ]]; then
    printf '\nRemove [1] artifacts only, [2] artifacts + UV targets, [q] quit? [1/2/q] '
    read -r answer || answer=q
    case "$answer" in
    1 | 2) choice=$answer ;;
    *)
        printf 'Cleanup cancelled.\n'
        exit 0
        ;;
    esac
elif [[ "$INCLUDE_UV_VENV" == true ]]; then
    choice=2
fi

declare -a TARGETS=()
if ((${#ARTIFACT_TARGETS[@]} > 0)); then
    TARGETS+=("${ARTIFACT_TARGETS[@]}")
fi
if [[ "$choice" == 2 ]] && ((${#UV_TARGETS[@]} > 0)); then
    TARGETS+=("${UV_TARGETS[@]}")
fi

if ((${#TARGETS[@]} == 0)); then
    printf '\nNothing to remove.\n'
    exit 0
fi

printf '\nRemoving %d path(s) ...\n' "${#TARGETS[@]}"
for target in "${TARGETS[@]}"; do
    rm -rf -- "$target"
done

printf 'Cleanup complete. Removed %d path(s).\n' "${#TARGETS[@]}"
