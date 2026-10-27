#!/usr/bin/env bash

# Create a new Git worktree for an Ink/Stitch branch, sharing the 'fonts'
# submodule with the main worktree via a symlink.
#
# Run with -h/--help (or press 'h' at the branch prompt) for a short help,
# including how to bring a branch from a remote or from a fork in locally.

set -eu

MAIN_WORKTREE_NAME='inkstitch'
SUBMODULE_PATH='fonts'
# Local Git config key marking that the help was shown for this repository.
HELP_SHOWN_MARKER='inkstitch.addWorktreeHelpShown'

usage() {
    printf 'Usage: %s [-h|--help]\n\n' "$0"
    printf '%s\n' \
        'Add a worktree for an Ink/Stitch branch (fonts submodule symlinked).' \
        'Run from the my_scripts symlink inside an Ink/Stitch worktree.' \
        '' \
        'Prompts:' \
        '  <number>  add a worktree for that local branch' \
        '  w         worktrees and branches without one' \
        '  r         remote branches' \
        '  h         this help' \
        '  q         quit' \
        '' \
        'Remote branches (option r):' \
        '  [n]   no local branch yet, pick one to fetch it in' \
        '  [--]  local branch already exists, not selectable' \
        '        (worktree) or (local) after the name says where it is' \
        '  f     filter the list by a substring (e.g. orig)' \
        '' \
        'After picking a remote branch:' \
        '  w  local tracking branch + worktree (default)' \
        '  t  local tracking branch only' \
        '  c  local branch with another name, no tracking' \
        '  b  back' \
        '' \
        'Manual equivalent (git pull is not needed, the new branch points at the remote):' \
        '  git fetch <remote>' \
        '  git branch --track <branch> <remote>/<branch>' \
        '  git worktree add <path> <branch>' \
        '' \
        'Or without a worktree (git >= 2.23, DWIM tracking):' \
        '  git switch <branch>' \
        '' \
        'Branch from a fork (once):' \
        '  git remote add fork <url>' \
        '  git fetch fork' \
        '' \
        'Single GitHub PR, no remote needed:' \
        '  git fetch origin pull/<n>/head:pr-<n>' \
        '' \
        'Refresh the listed branches first with: git fetch <remote>'
}

# Print the lines of a file as a numbered list, e.g. a list of branches. The
# numbers are padded so the names stay in one column.
numbered_list() {
    local number=0 item total width
    total=$(wc -l <"$1")
    width=${#total}
    while IFS= read -r item; do
        number=$((number + 1))
        printf '  [%*d] %s\n' "$width" "$number" "$item"
    done <"$1"
}

# Print the worktrees that already exist. The path and branch are aligned into
# two columns so the list stays readable even with long branch names.
show_worktrees() {
    local relative_path branch max_path=0 path_width arrow='->'
    printf '\n%s\n' 'Existing worktrees:'
    # First pass: find the longest path so the arrows line up in one column.
    while IFS=$'\t' read -r relative_path branch; do
        [ "${#relative_path}" -gt "$max_path" ] && max_path=${#relative_path}
    done <"$worktree_list_file"
    path_width=$((max_path + 1))
    while IFS=$'\t' read -r relative_path branch; do
        printf '  %-*s %s %s\n' "$path_width" "$relative_path" "$arrow" "$branch"
    done <"$worktree_list_file"
}

# Print the branches that do not have a worktree yet.
show_local_branches() {
    printf '\n%s\n' 'Branches without a worktree:'
    if [ "$branch_count" -eq 0 ]; then
        printf '  (none)\n'
    else
        numbered_list "$branch_list_file"
    fi
}

# Print the remote branches. Only the ones without a local branch are numbered
# and selectable; the others get a dashed placeholder so the branch names stay
# in one column and the same branch is not fetched in twice.
show_remote_branches() {
    local number=0 remote_branch status width dashes
    width=${#remote_count}
    dashes=$(printf '%*s' "$width" '' | tr ' ' '-')
    if [ -n "$remote_filter" ]; then
        printf '\nRemote branches (filter: %s):\n' "$remote_filter"
    else
        printf '\n%s\n' 'Remote branches:'
    fi
    while IFS=$'\t' read -r remote_branch status; do
        case "$status" in
        new)
            number=$((number + 1))
            printf '  [%*d] %s\n' "$width" "$number" "$remote_branch"
            ;;
        worktree)
            printf '  [%s] %s (worktree)\n' "$dashes" "$remote_branch"
            ;;
        local)
            printf '  [%s] %s (local)\n' "$dashes" "$remote_branch"
            ;;
        esac
    done <"$remote_filtered_list_file"
}

# Apply the current filter to the master remote lists, producing the filtered
# display and selectable lists plus the selectable count used for numbering.
apply_remote_filter() {
    if [ -z "$remote_filter" ]; then
        cp "$remote_list_file" "$remote_filtered_list_file"
        cp "$remote_selectable_file" "$remote_filtered_selectable_file"
    else
        grep -F -- "$remote_filter" "$remote_list_file" >"$remote_filtered_list_file" || true
        grep -F -- "$remote_filter" "$remote_selectable_file" >"$remote_filtered_selectable_file" || true
    fi
    remote_count=$(wc -l <"$remote_filtered_selectable_file")
}

# Print the worktrees and then the branches available for a new one.
show_lists() {
    show_worktrees
    show_local_branches
}

case "${1:-}" in
-h | --help)
    usage
    exit 0
    ;;
'') ;;
*)
    usage >&2
    exit 2
    ;;
esac

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

# List branches that are not already checked out in a worktree.
existing_branches=$(git -C "$repo_root" worktree list --porcelain | sed -n 's/^branch refs\/heads\///p')

branches_without_worktree=''
branch_count=0
for branch in $(git -C "$repo_root" branch --format='%(refname:short)'); do
    if ! printf '%s\n' "$existing_branches" | grep -qx "$branch"; then
        branches_without_worktree="$branches_without_worktree $branch"
        branch_count=$((branch_count + 1))
    fi
done

if [ "$branch_count" -eq 0 ]; then
    printf 'No branches without a worktree found; remote branches are still available with [r].\n'
fi

# Use helper files for safe iteration over branch and worktree names (handles
# spaces safely).
branch_list_file=$(mktemp)
local_all_file=$(mktemp)
remote_list_file=$(mktemp)
remote_selectable_file=$(mktemp)
remote_filtered_list_file=$(mktemp)
remote_filtered_selectable_file=$(mktemp)
worktree_list_file=$(mktemp)
trap 'rm -f "$branch_list_file" "$local_all_file" "$remote_list_file" "$remote_selectable_file" "$remote_filtered_list_file" "$remote_filtered_selectable_file" "$worktree_list_file"' EXIT

printf '%s\n' "$branches_without_worktree" | tr ' ' '\n' | grep -v '^$' >"$branch_list_file" || true
git -C "$repo_root" branch --format='%(refname:short)' >"$local_all_file"

# Show the existing worktrees and then the branches available for a new one.
# The porcelain listing puts "HEAD <sha>" before "branch <ref>" or "detached",
# so the entry is only complete once one of the latter two is seen.
worktree_path=''
git -C "$repo_root" worktree list --porcelain | while IFS= read -r line; do
    case "$line" in
    worktree*)
        worktree_path=${line#worktree }
        ;;
    branch*)
        branch_ref=${line#branch }
        relative_path=$(python3 -c "import os.path, sys; print(os.path.relpath(sys.argv[1], sys.argv[2]))" "$worktree_path" "$repo_root")
        printf '%s\t%s\n' "$relative_path" "${branch_ref#refs/heads/}" >>"$worktree_list_file"
        worktree_path=''
        ;;
    detached)
        relative_path=$(python3 -c "import os.path, sys; print(os.path.relpath(sys.argv[1], sys.argv[2]))" "$worktree_path" "$repo_root")
        printf '%s\t%s\n' "$relative_path" 'detached HEAD' >>"$worktree_list_file"
        worktree_path=''
        ;;
    esac
done
show_lists
# Option [r] lists the remote branches. A remote branch whose name already
# exists locally is marked and kept out of the selectable list, so the same
# branch is not fetched in twice.
git -C "$repo_root" for-each-ref --format='%(refname)' refs/remotes |
    sed -n 's|^refs/remotes/||p' |
    grep -v '/HEAD$' >"$remote_list_file.all" || true
while IFS= read -r remote_branch; do
    local_candidate=${remote_branch#*/}
    if printf '%s\n' "$existing_branches" | grep -qx "$local_candidate"; then
        status='worktree'
    elif grep -qx "$local_candidate" "$local_all_file"; then
        status='local'
    else
        status='new'
        printf '%s\n' "$remote_branch" >>"$remote_selectable_file"
    fi
    printf '%s\t%s\n' "$remote_branch" "$status" >>"$remote_list_file"
done <"$remote_list_file.all"
rm -f "$remote_list_file.all"
remote_filter=''
apply_remote_filter

# Show the help once per repository, on the first run, so the remote and fork
# workflow is visible without being intrusive on later runs.
help_shown=$(git -C "$repo_root" config --local --get "$HELP_SHOWN_MARKER" 2>/dev/null || true)
if [ -z "$help_shown" ]; then
    printf '\n'
    printf '%s\n' 'First run here, showing the help once:'
    printf '\n'
    usage
    printf '\n%s\n' 'Press [h] to see it again.'
    git -C "$repo_root" config --local "$HELP_SHOWN_MARKER" true
fi

selected_branch=''
while true; do
    printf 'Select branch by number ([w] worktrees, [r] remote, [h] help, [q] quit): '
    read -r selection

    case "$selection" in
    q | Q)
        printf 'Aborted.\n'
        exit 0
        ;;
    h | H)
        printf '\n'
        usage
        printf '\n'
        continue
        ;;
    w | W)
        show_lists
        continue
        ;;
    r | R)
        while true; do
            if [ "$remote_count" -eq 0 ]; then
                if [ -n "$remote_filter" ]; then
                    printf 'No remote branches match the filter "%s".\n' "$remote_filter"
                    remote_filter=''
                    apply_remote_filter
                else
                    printf 'All remote branches already have a local branch.\n'
                fi
                if [ "$remote_count" -eq 0 ]; then
                    show_lists
                    break
                fi
            fi

            show_remote_branches
            printf '\n'
            printf '%s\n' \
                'A number creates a local branch from that remote branch; you then' \
                'choose the worktree, tracking, or another local name.'
            printf 'Select remote branch by number ([f] filter, [b] back, q to quit): '
            read -r remote_selection

            case "$remote_selection" in
            q | Q)
                printf 'Aborted.\n'
                exit 0
                ;;
            b | B)
                show_lists
                break
                ;;
            f | F)
                if [ -n "$remote_filter" ]; then
                    read -p 'Filter substring (edit, or clear and press Enter to reset): ' -e -i "$remote_filter" -r remote_filter
                else
                    read -p 'Filter substring (e.g. orig): ' -r remote_filter
                fi
                apply_remote_filter
                continue
                ;;
            esac

            if ! printf '%s\n' "$remote_selection" | grep -Eq '^[0-9]+$'; then
                printf 'Invalid input.\n'
                continue
            fi

            if [ "$remote_selection" -lt 1 ] || [ "$remote_selection" -gt "$remote_count" ]; then
                printf 'Selection out of range.\n'
                continue
            fi

            remote_branch=$(sed -n "${remote_selection}p" "$remote_filtered_selectable_file")
            remote_name=${remote_branch%%/*}
            remote_branch_name=${remote_branch#*/}
            # The remote-tracking ref can be stale; make sure the branch is known.
            git -C "$repo_root" fetch "$remote_name"
            if ! git -C "$repo_root" rev-parse --verify --quiet "refs/remotes/$remote_branch" >/dev/null; then
                printf 'Error: remote branch "%s" does not exist (anymore).\n' "$remote_branch" >&2
                continue
            fi

            local_name="$remote_branch_name"
            if git -C "$repo_root" show-ref --verify --quiet "refs/heads/$local_name"; then
                printf 'Error: local branch "%s" already exists.\n' "$local_name" >&2
                continue
            fi

            printf '\n'
            printf '%s\n' \
                "Remote branch: $remote_branch" \
                "Local branch:  $local_name" \
                '  [w] tracking branch + worktree (default)' \
                '  [t] tracking branch only' \
                '  [c] another local name, no tracking' \
                '  [b] back'
            printf 'Action [w]: '
            read -r remote_action

            case "$remote_action" in
            b | B)
                show_lists
                break
                ;;
            t | T)
                printf 'Creating local tracking branch %s for %s...\n' "$local_name" "$remote_branch"
                git -C "$repo_root" branch --track "$local_name" "$remote_branch"
                printf 'Done. Branch %s tracks %s. No worktree was created.\n' "$local_name" "$remote_branch"
                exit 0
                ;;
            c | C)
                read -p "Local branch name (edit with arrows) [$local_name]: " -e -i "$local_name" -r renamed_local
                renamed_local=${renamed_local:-$local_name}
                clean_local=$(printf '%s' "$renamed_local" | sed 's/[^A-Za-z0-9._/-]/-/g')
                if [ -z "$clean_local" ] || git -C "$repo_root" show-ref --verify --quiet "refs/heads/$clean_local"; then
                    printf 'Error: invalid or already existing branch name "%s".\n' "$renamed_local" >&2
                    continue
                fi
                local_name="$clean_local"
                printf 'Creating local branch %s at %s (without tracking)...\n' "$local_name" "$remote_branch"
                git -C "$repo_root" branch --no-track "$local_name" "$remote_branch"
                ;;
            w | W | '')
                printf 'Creating local tracking branch %s for %s...\n' "$local_name" "$remote_branch"
                git -C "$repo_root" branch --track "$local_name" "$remote_branch"
                ;;
            *)
                printf 'Invalid input.\n'
                continue
                ;;
            esac

            selected_branch="$local_name"
            break 2
        done
        if [ -n "$selected_branch" ]; then
            break
        fi
        ;;
    esac

    if ! printf '%s\n' "$selection" | grep -Eq '^[0-9]+$'; then
        printf 'Invalid input.\n'
        continue
    fi

    if [ "$selection" -lt 1 ] || [ "$selection" -gt "$branch_count" ]; then
        printf 'Selection out of range.\n'
        continue
    fi

    break
done

# Resolve the selected branch, unless it was already created above from a
# remote branch.
if [ -z "$selected_branch" ]; then
    selected_branch=$(sed -n "${selection}p" "$branch_list_file")
fi

# Suggest a worktree directory name based on the branch.
suggested_name=$(printf '%s' "wt-$selected_branch" | sed 's/\//-/g')
read -p "Worktree directory name [$suggested_name]: " -e -i "$suggested_name" -r chosen_name
chosen_name=${chosen_name:-$suggested_name}

# Sanitize the name.
clean_name=$(printf '%s' "$chosen_name" | sed 's/[^A-Za-z0-9._-]/-/g')
if [ -z "$clean_name" ]; then
    printf 'Invalid worktree directory name.\n' >&2
    exit 1
fi

new_worktree_path="$worktrees_parent/$clean_name"

if [ -e "$new_worktree_path" ]; then
    printf 'Error: "%s" already exists.\n' "$new_worktree_path" >&2
    exit 1
fi

# Create the worktree.
printf 'Creating worktree %s for branch %s...\n' "$new_worktree_path" "$selected_branch"
git -C "$repo_root" worktree add "$new_worktree_path" "$selected_branch"

# Only if fonts is tracked as a submodule (gitlink) in the new worktree, replace
# it with a symlink to the main worktree and mark it assume-unchanged. If fonts
# is not part of this worktree, do nothing.
if git -C "$new_worktree_path" ls-files --stage "$SUBMODULE_PATH" | grep -q '^160000'; then
    printf 'Linking %s to main worktree...\n' "$SUBMODULE_PATH"
    rm -rf "$new_worktree_path/$SUBMODULE_PATH"
    ln -s "../$MAIN_WORKTREE_NAME/$SUBMODULE_PATH" "$new_worktree_path/$SUBMODULE_PATH"
    git -C "$new_worktree_path" update-index --assume-unchanged "$SUBMODULE_PATH"
fi

printf 'Done. New worktree is ready at:\n  %s\n' "$new_worktree_path"
