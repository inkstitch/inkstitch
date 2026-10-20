# Development worktrees and uv

These helpers make it quicker to test multiple Ink/Stitch branches side by side.
Each worktree has its own Git checkout and `.venv`; the `fonts` submodule is
shared from the main checkout through a symlink.

The worktree scripts expect the main checkout to be a sibling directory named
`inkstitch`, with the `fonts` submodule initialized. For example:

```text
inkstitch/                 # main checkout, including fonts/
wt-010-branch-name-1/      # first worktree
wt-020-another-branch-2/   # second worktree
```

Run the commands below from the root of the relevant worktree.

## Create and manage worktrees

Create a worktree for a local branch:

```sh
cd /path/to/inkstitch
bash dev/worktree/010_add_worktree.sh
```

The script offers local branches without a worktree and remote branches. For a
remote branch, choose `r`, select the branch, and accept the default action to
create a local tracking branch and its worktree. The suggested directory name
is `wt-` followed by the branch name, with `/` replaced by `-`. Use `-h` for
the full interactive help. Fetch remotes first if their branch lists may be
stale. At the directory-name prompt, replace the branch-based suggestion with
a name such as `wt-010-branch-name-1`: keep a short branch name in the middle
and increment the final number for each new worktree to keep them in creation
order.

Other worktree helpers:

```sh
bash dev/worktree/030_rename_worktree.sh
bash dev/worktree/020_remove_worktree.sh
bash dev/worktree/040_rebuild_font_symlink.sh
```

Rename and remove operate on another worktree selected from a list; they do not
rename or remove the main checkout. **Removal runs `git worktree remove
--force`**, so commit or stash any changes in the selected worktree first. The
font repair script replaces the current `fonts` entry with a symlink to
`../inkstitch/fonts`; use it only when the main checkout has the submodule
initialized.

The worktree scripts do not clean up branches automatically. After removing a
worktree, prune deleted remote branches and delete its local branch manually:

```sh
git fetch --prune
git branch -D branch-name
```

Use `-D` only when you are sure the branch has no unmerged work you need; it
force-deletes the local branch.

## Set up a worktree's Python environment

Set up the environment separately in each worktree. This keeps dependencies
available when switching branches without reinstalling them:

```sh
cd /path/to/wt-010-branch-name-1
bash dev/uv/020_setup_uv_venv.sh --py 3.13
```

The script creates `.venv`, pins the selected Python version, syncs project
dependencies with `uv`, and runs `make inx`. It defaults to Python 3.13. The
current project requires Python 3.11 or newer; pass a compatible version with
`--py VERSION` (or `--py=VERSION`). On Linux it selects a distro-specific
prebuilt wxPython wheel for the distributions it recognizes, to avoid building
wxPython from source. Wheel availability can vary by distribution and version.
macOS and Windows use the normal package index; Windows should be run from Git
Bash, MSYS2, or WSL.

If an environment already exists, the script asks before setting it up again.
`--yes` skips the prompt and **deletes the existing `.venv` before recreating
it**:

```sh
bash dev/uv/020_setup_uv_venv.sh --yes --py 3.13
```

## Test the worktree in Inkscape

Installing `uvr` is optional. It lets Inkscape run different Python
extensions with their own virtual environments, so extensions that need
different Python dependencies can be used side by side. Install it with `uv`:

```sh
uv tool install uvr
```

From the worktree you want to test, run:

```sh
bash dev/uv/030_activate_in_inkscape.sh
```

This links the worktree into the Inkscape user extensions directory using the
`dev` postfix by default. When available, the script configures Inkscape to use
the `uvr` launcher; otherwise, it falls back to that worktree's `.venv` Python.
Pass `--use-python` to select the `.venv` explicitly. Run `--help` for options
such as a different postfix or Inkscape configuration directory. The script
also reports a system-wide Ink/Stitch installation that may be loaded alongside
the development extension.

## Clean generated files

The cleanup script first lists its targets and prompts for a choice:

```sh
bash dev/uv/010_cleanup_uv.sh
```

Choose option 1 to remove generated artifacts outside `.venv`, or option 2 to
also remove `.venv`, `uv.lock`, and `.python-version`. For non-interactive use,
`--yes` removes generated artifacts only; `--yes --uv` includes the uv files as
well:

```sh
bash dev/uv/010_cleanup_uv.sh --yes --uv
```

## Rebase worktrees after a PR is merged

After a PR is merged, update the main checkout (assumed to be on `main`):

```sh
cd /path/to/inkstitch
git pull --ff-only
```

Then, in each worktree that should include the updated `main`, check whether it
has commits to rebase onto:

```sh
git log HEAD..main --oneline
```

If the command lists commits, rebase the worktree onto `main`:

```sh
git rebase main
```

If conflicts occur, either cancel the in-progress rebase or resolve the
conflicts, stage the resolved files, and continue:

```sh
git rebase --abort
# or, after resolving conflicts:
git add <resolved-files>
git rebase --continue
```

To restore the branch to its pre-rebase commit after the rebase has finished,
use `git reset --hard ORIG_HEAD`. This discards uncommitted changes, so check
the worktree first.

Rebasing rewrites the branch history. Update its remote PR branch with
`--force-with-lease`, which refuses to overwrite remote commits you have not
fetched; this push also triggers push-based GitHub Actions:

```sh
git push --force-with-lease
```
