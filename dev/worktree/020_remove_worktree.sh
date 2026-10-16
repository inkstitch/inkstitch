#!/usr/bin/env bash

# Remove an existing Git worktree for the Ink/Stitch repository.
#
# Usage:
#   cd /path/to/inkstitch-worktree/my_scripts
#   ./worktree/020_remove_worktree.sh
#
# The script must be run from the my_scripts symlink inside an Ink/Stitch
# worktree so it can locate the correct repository root.

set -eu

script_dir=$(dirname "$0")

case "$script_dir" in
/*) resolved_script_dir="$script_dir" ;;
*) resolved_script_dir="$PWD/$script_dir" ;;
esac

candidate_root_a=$(cd "$resolved_script_dir/../.." 2>/dev/null && git rev-parse --show-toplevel 2>/dev/null || true)
candidate_root_b=$(cd "$(dirname "$PWD")" 2>/dev/null && git rev-parse --show-toplevel 2>/dev/null || true)

repo_root=''
for candidate in "$candidate_root_a" "$candidate_root_b"; do
    if [ -n "$candidate" ] && [ -f "$candidate/.gitmodules" ]; then
        repo_root="$candidate"
        break
    fi
done

if [ -z "$repo_root" ]; then
    printf '%s\n' \
        'Error: no Ink/Stitch worktree was found.' \
        'Run this script from the my_scripts symlink in an Ink/Stitch worktree.' >&2
    exit 1
fi

worktrees_parent=$(dirname "$repo_root")

# Collect removable worktrees (exclude the main worktree and locked worktrees).
worktree_list_file=$(mktemp)
trap 'rm -f "$worktree_list_file"' EXIT

git -C "$repo_root" worktree list --porcelain | while IFS= read -r line; do
    case "$line" in
    worktree*)
        worktree_path=${line#worktree }
        branch_ref=''
        ;;
    branch*)
        branch_ref=${line#branch refs/heads/}
        ;;
    HEAD*)
        branch_ref=${line#HEAD }
        branch_ref="detached${branch_ref:+ ${branch_ref}}"
        ;;
    locked*)
        if [ -n "$worktree_path" ]; then
            printf '%s\t%s\tlocked\n' "$worktree_path" "${branch_ref:-detached}" >>"$worktree_list_file"
            worktree_path=''
        fi
        ;;
    *)
        if [ -n "$worktree_path" ]; then
            printf '%s\t%s\t%s\n' "$worktree_path" "${branch_ref:-detached}" "unlocked" >>"$worktree_list_file"
            worktree_path=''
        fi
        ;;
    esac
done

# Remove the trailing empty block delimiter and entries for the main worktree.
if [ ! -s "$worktree_list_file" ]; then
    printf 'No removable worktrees found.\n'
    exit 0
fi

# The main worktree cannot be removed.
removable_file=$(mktemp)
trap 'rm -f "$removable_file"' EXIT

while IFS=$'\t' read -r path branch state; do
    [ "$path" = "$repo_root" ] && continue
    relative_path=$(python3 -c "import os.path, sys; print(os.path.relpath(sys.argv[1], sys.argv[2]))" "$path" "$repo_root")
    printf '%s\t%s\t%s\t%s\n' "$path" "$relative_path" "$branch" "$state" >>"$removable_file"
done <"$worktree_list_file"

if [ ! -s "$removable_file" ]; then
    printf 'No removable worktrees found.\n'
    exit 0
fi

printf '%s\n' 'Existing worktrees (except main):'
line_count=0
while IFS=$'\t' read -r path relative_path branch state; do
    line_count=$((line_count + 1))
    printf '  [%d] %s -> %s' "$line_count" "$relative_path" "$branch"
    if [ "$state" = 'locked' ]; then
        printf ' (locked)\n'
    else
        printf '\n'
    fi
done <"$removable_file"

while true; do
    printf 'Select worktree to remove by number (or q to quit): '
    read -r selection

    if [ "$selection" = 'q' ] || [ "$selection" = 'Q' ]; then
        printf 'Aborted.\n'
        exit 0
    fi

    if ! printf '%s\n' "$selection" | grep -Eq '^[0-9]+$'; then
        printf 'Invalid input.\n'
        continue
    fi

    if [ "$selection" -lt 1 ] || [ "$selection" -gt "$line_count" ]; then
        printf 'Selection out of range.\n'
        continue
    fi

    break
done

selected_path=$(sed -n "${selection}p" "$removable_file" | cut -f1)
selected_relative=$(sed -n "${selection}p" "$removable_file" | cut -f2)

printf 'Are you sure you want to remove worktree "%s"? [y/N]: ' "$selected_relative"
read -r confirm

if [ "$confirm" != 'y' ] && [ "$confirm" != 'Y' ]; then
    printf 'Aborted.\n'
    exit 0
fi

printf 'Removing worktree %s...\n' "$selected_relative"
git -C "$repo_root" worktree remove --force "$selected_path"
printf 'Done.\n'
