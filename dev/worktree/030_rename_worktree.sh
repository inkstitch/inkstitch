#!/usr/bin/env bash

# Rename an existing Git worktree directory for the Ink/Stitch repository.
#
# Usage:
#   cd /path/to/inkstitch-worktree/my_scripts
#   ./worktree/030_rename_worktree.sh
#
# The script must be run from the my_scripts symlink inside an Ink/Stitch
# worktree so it can locate the correct repository root.

set -eu

MAIN_WORKTREE_NAME='inkstitch'
SUBMODULE_PATH='fonts'

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
main_worktree_path="$worktrees_parent/$MAIN_WORKTREE_NAME"

# Collect all worktrees (except the main worktree, which cannot be moved via git worktree move).
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
    *)
        if [ -n "$worktree_path" ]; then
            printf '%s\t%s\n' "$worktree_path" "${branch_ref:-detached}" >>"$worktree_list_file"
            worktree_path=''
        fi
        ;;
    esac
done

movable_file=$(mktemp)
trap 'rm -f "$movable_file"' EXIT

while IFS=$'\t' read -r path branch; do
    [ "$path" = "$repo_root" ] && continue
    relative_path=$(python3 -c "import os.path, sys; print(os.path.relpath(sys.argv[1], sys.argv[2]))" "$path" "$repo_root")
    printf '%s\t%s\t%s\n' "$path" "$relative_path" "$branch" >>"$movable_file"
done <"$worktree_list_file"

if [ ! -s "$movable_file" ]; then
    printf 'No movable worktrees found.\n'
    exit 0
fi

printf '%s\n' 'Existing worktrees (except main):'
line_count=0
while IFS=$'\t' read -r path relative_path branch; do
    line_count=$((line_count + 1))
    printf '  [%d] %s -> %s\n' "$line_count" "$relative_path" "$branch"
done <"$movable_file"

while true; do
    printf 'Select worktree to rename by number (or q to quit): '
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

selected_path=$(sed -n "${selection}p" "$movable_file" | cut -f1)
selected_relative=$(sed -n "${selection}p" "$movable_file" | cut -f2)
selected_name=$(basename "$selected_path")

printf 'Current worktree directory name (edit with arrows): %s\n' "$selected_name"
read -e -i "$selected_name" -p 'New worktree directory name: ' new_name
new_name=${new_name:-$selected_name}

# Sanitize the name.
clean_name=$(printf '%s' "$new_name" | sed 's/[^A-Za-z0-9._-]/-/g')
if [ -z "$clean_name" ]; then
    printf 'Invalid worktree directory name.\n' >&2
    exit 1
fi

new_worktree_path="$worktrees_parent/$clean_name"

if [ -e "$new_worktree_path" ]; then
    printf 'Error: "%s" already exists.\n' "$new_worktree_path" >&2
    exit 1
fi

# Temporarily remove a fonts symlink so Git does not see a submodule inside the
# worktree during the move. The symlink is restored right after the move.
fonts_symlink_target=''
if [ -L "$selected_path/$SUBMODULE_PATH" ]; then
    fonts_symlink_target=$(readlink "$selected_path/$SUBMODULE_PATH")
    printf 'Temporarily moving %s symlink aside...\n' "$SUBMODULE_PATH"
    rm "$selected_path/$SUBMODULE_PATH"
fi

printf 'Renaming worktree %s to %s...\n' "$selected_relative" "$clean_name"
git -C "$repo_root" worktree move "$selected_path" "$new_worktree_path"

# Restore the fonts symlink pointing to the original target if possible,
# otherwise fall back to the main worktree fonts directory.
if [ -n "$fonts_symlink_target" ]; then
    printf 'Restoring %s symlink...\n' "$SUBMODULE_PATH"
    rm -rf "$new_worktree_path/$SUBMODULE_PATH"
    ln -s "$fonts_symlink_target" "$new_worktree_path/$SUBMODULE_PATH"
    git -C "$new_worktree_path" update-index --skip-worktree "$SUBMODULE_PATH"
fi

printf 'Done.\n'
