#!/usr/bin/env bash

# Rebuild the 'fonts' symlink in an Ink/Stitch worktree after it has been
# broken (e.g. by a rebase that reset the submodule gitlink back to an empty
# directory).
#
# Usage:
#   cd /path/to/inkstitch-worktree/my_scripts
#   ./worktree/040_rebuild_font_symlink.sh
#
# The script must be run from the my_scripts symlink inside an Ink/Stitch
# worktree so it can locate the correct repository root. It is idempotent:
# if the symlink is already correct, it does nothing.

set -eu

MAIN_WORKTREE_NAME='inkstitch'
SUBMODULE_PATH='fonts'

script_dir=$(dirname "$0")

# Resolve the script path to a physical directory (symlinks are resolved so we
# can climb out of the shared my_scripts folder).
case "$script_dir" in
/*) resolved_script_dir="$script_dir" ;;
*) resolved_script_dir="$PWD/$script_dir" ;;
esac

# Try two candidate roots:
# 1. Two directories above the script (my_scripts/worktree -> worktree root).
# 2. The directory above the current directory (my_scripts symlink -> worktree root).
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

# The worktrees share a parent directory. The main worktree is a sibling.
worktrees_parent=$(dirname "$repo_root")
main_worktree_path="$worktrees_parent/$MAIN_WORKTREE_NAME"

if [ ! -d "$main_worktree_path/$SUBMODULE_PATH" ]; then
    printf 'Error: main worktree "%s" does not contain the "%s" submodule.\n' \
        "$main_worktree_path" "$SUBMODULE_PATH" >&2
    printf 'Initialize it first in the main worktree with:\n  git submodule update --init %s\n' \
        "$SUBMODULE_PATH" >&2
    exit 1
fi

# Only act if fonts is tracked as a submodule (gitlink) in this worktree.
if ! git -C "$repo_root" ls-files --stage "$SUBMODULE_PATH" | grep -q '^160000'; then
    printf '"%s" is not tracked as a submodule in this worktree; nothing to do.\n' \
        "$SUBMODULE_PATH"
    exit 0
fi

target_link="../$MAIN_WORKTREE_NAME/$SUBMODULE_PATH"

# Already correct? Nothing to do.
if [ -L "$repo_root/$SUBMODULE_PATH" ] && [ "$(readlink "$repo_root/$SUBMODULE_PATH")" = "$target_link" ]; then
    printf '"%s" is already a correct symlink; nothing to do.\n' "$SUBMODULE_PATH"
    exit 0
fi

# Rebuild the symlink, replacing whatever is currently there (empty dir, broken
# link, or a real checkout).
printf 'Rebuilding %s symlink -> %s...\n' "$SUBMODULE_PATH" "$target_link"
rm -rf "$repo_root/$SUBMODULE_PATH"
ln -s "$target_link" "$repo_root/$SUBMODULE_PATH"
git -C "$repo_root" update-index --assume-unchanged "$SUBMODULE_PATH"

printf 'Done. %s is now a symlink to the main worktree.\n' "$SUBMODULE_PATH"
