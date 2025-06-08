

# Proposal: Accelerating and Modernizing InkStitch Dependency Management with `uv` and `pyproject.toml`

This proposal outlines how to migrate InkStitch's Python dependency management to `uv` for faster, more reliable, and reproducible builds.

While there are indeed many excellent `Python` package managers out there (`Poetry`, `PDM`, `Hatch`, `Pipenv`, etc.), `uv` stands out primarily because of its unmatched speed.

## Quick Start Guide

1. **Install uv & Setup Environment**:

  *  Install uv (e.g., `curl -LsSf https://astral.sh/uv/install.sh | sh`).
  *  In your InkStitch project: `... uv venv ...`
  *  Install dependencies: `... uv sync ...`
  *  Activate the environment: `source .venv/bin/activate`

2. **Run Inkscape**:

  *  (Optional) Update Inkscape extension files: `make inx`
  *  (Optional) Update Inkscape config (`~/.config/inkscape/preferences.xml`) with `python-interpreter="/path/to/.venv/bin/python"`.
  *  Run Inkscape from this activated environment.



## Why UV?

* **Extremely Fast:**
Offers blazing-fast dependency resolution and package installation. This speed is significantly boosted by its efficient caching system. When the cache resides on the same disk as your project's virtual environment, `uv` uses hard links to avoid copying packages, making installations nearly instantaneous. If on a different disk, packages must be copied, which is still fast, but not quite as immediate.

* **Written in Rust, Self-Contained**: Because `uv` is written in `Rust`, you don't need to install `Python` on your system to run `uv` itself. This makes `uv` incredibly easy to bootstrap and integrate, simplifying initial setup across different environments.

* **Manages Python Itself**: `uv` can directly acquire and manage specific Python versions, eliminating the need for separate tools like `pyenv` or `conda` for basic Python installations. This simplifies setup and ensures consistency.

* **Enhanced Portability**: By managing its own Python installations and robustly resolving dependencies, `uv` significantly simplifies cross-platform deployment and ensures consistency across various operating systems. This makes InkStitch more portable.

* **Simple Cache Setup for GitHub Actions**: Integrating uv's robust caching into GitHub Actions workflow is simple and will significantly accelerate build times.


## Resources

* **pyproject.toml** definition
  * https://packaging.python.org/en/latest/specifications/pyproject-toml/

* **Dependency specifiers**
  * https://packaging.python.org/en/latest/specifications/dependency-specifiers/

* **uv** project manager
  * https://github.com/astral-sh/uv

* **uvr** run specific uv managed scripts
  * https://github.com/karnigen/uvr


## How activate UV environment?

Refer to the following scripts for implementation details:
```Bash
bin/uv/uv_tools_install.sh
bin/uv/uv_tools_update.sh
```

Let's dive into how `uv` can be specifically applied to **InkStitch**, assuming the reader is already familiar with `uv`'s basics.



* **Installation uv**: see https://github.com/astral-sh/uv
 and use direct download.

   * Linux, MacOS
   `curl -LsSf https://astral.sh/uv/install.sh | sh`
   * Windows `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`


* **Install tools**:
`uv tool install` command lets you install Python-based command-line utilities into isolated environments. This makes tools like linters (`Ruff`), build systems like `CMake`, or other utilities accessible from anywhere on your system without cluttering your global Python setup.
  * Ensure the tools' installation path is in your PATH.

  ```Bash
  uv tool install --from git+https://github.com/karnigen/uvr uvr
  uv tool install ruff
  uv tool install flake8
  uv tool install cmake
  ```
* **Use Worktree**: Worktrees are a neat **Git** feature that let you have multiple working directories, each with a different branch checked out, all sharing the same **Git** repository's history. Think of it as having several separate workspaces for one project *without* creating multiple *full clones*.

* **Creating a Git Worktree**
  * **Go to main repo**: `cd /path/to/your/inkstitch`
  * **Add new worktree**:
    *  *Existing branch*: `git worktree add ../new-dir existing-branch`
    *  *New branch*: `git worktree add ../new-dir -b new-branch`
    *  *Specific commit*: `git worktree add ../new-dir HEAD~3`
  * **Verify**: `git worktree list`

* Set **Python version** and install packages:
  * **Go to** your InkStitch main repo or worktree directory:
    ```Bash
    cd /path/to/your/worktree
    ```
  * **List** available pythons:
    ```Bash
    uv python list
    ```
  * **Set** python version:
    ```Bash
    uv python pin 311
    ```
  * **Create** virtual environment (`.venv` directory):
    ```Bash
    uv venv
    ```
  * **Install** local packages, using `uv pip` subsystem: Using `uv pip` does not modify `pyproject.toml`, avoid using `uv add` that modify `pyproject.toml` for everyone. `pyproject.toml` must be kept unified across all platforms and OS's.
    ```Bash
    uv pip install my_package

    # prebuild wxpython for linux64 (Ubuntu 22.04 Python 311)
    uv pip install "https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-22.04/wxpython-4.2.3-cp311-cp311-linux_x86_64.whl"

    uv pip my_debugger
    ```
  * **Install** packages from `pyproject.toml`:
    ```Bash
    uv sync --inexact
    ```

    Using `uv sync` without `--inexact` removes all packages installed via `uv pip install` that are not specified in `pyproject.toml`, leaving only those explicitly defined.

  * **Activate** virtual environment:
    ```Bash
    . .venv/bin.activate
    ```
  * You may need to **update** Inkscape's extension files by running:
    ```Bash
    make inx
    ```

  * Ensure you run **Inkscape** from within this activated Python virtual environment.

    * You might also need to update Inkscape's configuration file, `~/.config/inkscape/preferences.xml`, specifically the key `python-interpreter="/path/to/.venv/bin/python"`


## Adjustments in `git` and `pyproject.toml`

Here's an overview of the key changes related to Git and Python dependency management:


### PyEmbroidery Integration

  * **`pyembroidery` Removal**: We're removing pyembroidery as both a relative dependency in requirements.txt and as a **Git** submodule.
  * **On-the-fly Inclusion**: pyembroidery will now be included directly as a package reference from its **Git** repository in `pyproject.toml`:
    * `"pyembroidery @ git+https://github.com/inkstitch/pyembroidery"`
    * This eliminates the need for it to be a PyPI package.

### Dependency File Synchronization

  * **Maintaining Both Files**: We'll keep `requirements.txt` and `pyproject.toml` synchronized for backward compatibility.
  * **Format Differences**: The formats vary minimally (e.g., numpy in `requirements.txt` vs. "numpy", in `pyproject.toml`).
  * **uv Support**: `uv` supports installing from both file types:
    * `uv pip install -r requirements.txt` or
    * `uv pip install -r pyproject.toml`.

### PyGObject Introspection (OS-Dependent)

  * **Requirement**: PyGObject is essential for `inkex` and `wxPython`.
  * **OS/GTK Dependency**: Versions greater than 3.50 require the latest GTK (e.g., in Ubuntu 24.04), which could necessitate a full OS reinstallation.
  * **No OS Version Targeting**: pyproject.toml lacks a way to identify specific OS versions for conditional dependencies.
  * **Version Pinning**: Therefore, PyGObject is pinned to version <=3.50 to maintain broader compatibility.


## General Rules `pyproject.toml`


Understanding these rules for pyproject.toml helps maintain a smooth and efficient development process:

### Location & Caching

  * **Top-Level Requirement**: `pyproject.toml` must be in the top-level directory of your project. This is essential for package creation (even for on-the-fly packaging) and for `uv` to correctly detect your project's dependencies.
  * **Cache Invalidation**: The hash of `pyproject.toml` is used as a cache identifier in GitHub Actions workflows. Any change to pyproject.toml will trigger a cache miss, leading to a full rebuild of all packages.
  * **Avoid Unnecessary Changes**: Don't unnecessarily change or pin package versions in `pyproject.toml` simply because a build crashed. Crashes are often caused by package updates on **PyPI**, and blindly pinning versions can consume significant time. Investigate the root cause first.


### Version Control & Precedence

  * **.gitignore Configuration**: Currently, `.python-version` and `uv.lock` are ignored in .gitignore.
  * **uv.lock Precedence**: Be aware that `uv.lock` has higher precedence than `pyproject.toml`. This means that even if you change version requirements in `pyproject.toml`, `uv` might ignore them if a `uv.lock` file is present, as it prioritizes the exact versions specified in the lock file for reproducibility.


## Makefile Updates

While we'll cover Makefile specifics in more detail later, here are some immediate highlights:

  * **uname Behavior in Docker**: The `uname` command might not return the actual operating system of the **Docker** container, as it reflects the host's kernel. This requires a solution for accurate OS detection within builds (maybe `lsb_release`).
  * **Adjusted Rules**: Some `Makefile` rules have been refined, and we've added `make help` for command overview and `make ignored` to list files not tracked by Git (outside of .gitignore).
  * **make manual**: This rule is currently not in use and serves as an alias for `make inx`.

  * **messages.po**:  This target was intended for localization (L10n), used to extract translatable strings into .po files. **However, it appears this target is currently not actively used in the development workflow ?!?**



## GitHub Workflow Action Updates

We've significantly overhauled InkStitch GitHub Actions CI/CD system to streamline builds, improve maintainability, and reduce strain on GitHub resources.


### New Build System Structure

* **Modular CI/CD for Multi-OS Builds**: A completely new CI/CD system for InkStitch builds across various operating systems and architectures has been implemented using reusable workflows. This is encapsulated in `uv_build.yml`.

* **Simplified Maintenance**: The monolithic `build.yml` file has been replaced by several dedicated workflow files for clarity and easier maintenance:
  * `uv_build.yml` (the reusable entry point)
  * `uv_build_linux32.yml`
  * `uv_build_linux64.yml`
  * `uv_build_linuxarm64.yml`
  * `uv_build_macarm64.yml`
  * `uv_build_macx86.yml`
  * `uv_build_windows64.yml`

* This modularity allows for easy `diff` comparisons, for example, to quickly see differences between `linux64` and `linux arm64` builds.



### Controlled Build Activation
* **Reduced GitHub Load**: To minimize strain on GitHub resources, we've designed a system to activate full package builds using an external script leveraging the **gh client** (https://cli.github.com/).

* **Optimized Build Triggers**: A full package build for all operating systems is typically unnecessary after every **push**. Instead, routine pushes will focus on **checks and tests**. Full builds should only be triggered when changes are finalized and ready for installation package creation.

* **Activation Command**: Full builds can now be triggered manually using the **gh CLI**:
  ```Bash
  gh workflow run $WF -r $BR -f build_type=$build_type -f break_on=$break_on -f input_tag=$tag
  ```
  * **$WF**: The specific .yml workflow file to invoke (e.g., uv_build.yml).
  * **$BR**: The current branch (e.g., `git rev-parse --abbrev-ref HEAD`).
  * **build_type**: Specifies the target build(s): `dummy, linux64, linuxarm64, linux32, windows64, macx86, macarm64`, or `all`.
  * **break_on**: Allows for early termination during the build process:
      * `no`: Normal execution.
      * `uv`: Stops after uv installation and cache check.
      * `sync`: Stops after package installation.
  * **input_tag**: The tag under which to store the resulting build artifacts.

Example of `gh` script (see `bin/uv/gh_action_run.sh`):
```Bash
set -x

WF=uv_build.yml
BR=`git rev-parse --abbrev-ref HEAD`  # branch

build_type='dummy'
# build_type='linux32'
# build_type='linux64'
# build_type='linuxarm64'
# build_type='macarm64'
# build_type='macx86'
# build_type='windows64'
# build_type='all'

break_on="no"
# break_on="uv"
# break_on="sync"

# tag='dev-build-$BR'

# git commit -a -m "Automated Commit & Build"
# git push

# gh workflow run $WF -r $BR -f build_type=$build_type -f break_on=$break_on -f input_tag=$tag
gh workflow run $WF -r $BR -f build_type=$build_type -f break_on=$break_on
```

* **Tag-Based Activation**: The `uv_build.yml` workflow can also be activated by specific Git tags:

  * **vX.X.X***: Triggers a release build with `build_type=all`.
  * **build***: Initiates a **dummy** build, primarily for verifying the entire process and creating a record in GitHub Actions. This is crucial for using the *gh CLI*, as workflows callable by `gh` must have at least one previous run (unless called on main or master branches).


## Release TAG_NAME

Here's how release naming and artifact storage work in our workflow:

* **Artifact Storage**: For each workflow run, output files can be stored in the GitHub Releases section under a chosen name.
* **InkStitch Naming Convention**: InkStitch uses the following patterns for release names:
  * `dev-build-branch-name` (for development builds)
  * `vX.X.X...` (for official versioned releases)
* **Incremental Builds**: This storage method is permanent, enabling incremental builds. We can, for example, first compile for `macx86`, then for `linux64`, and the compiled files will progressively accumulate in the release repository.
* **Temporary Job Artifacts**: During a single job run, intermediate results and artifacts are stored in the workflow run's dedicated artifact storage, which is temporary (usually kept for 90 days or less, depending on repository settings), not directly in *GitHub Releases*.


## Cache Pitfalls in GitHub Actions

Caching in GitHub Actions can significantly speed up your workflows, but it's crucial to understand how it works to avoid common pitfalls. Misconfigured caches can lead to unexpected rebuilds or incorrect data.

### How Caching Works

The core principle of caching in GitHub Actions involves these steps:

  * **Cache Key Definition**: You define a cache key (a unique name) for your cache. This key is used to identify and retrieve a specific cache.
  * **Cache Lookup**: The system checks if a cache with the specified key already exists.
  * **Cache Restoration (if found)**: If a matching cache is found, its contents are restored to a designated location (mount point) within your workflow's runner environment (e.g., your Docker container).
  * **Cache Saving (if needed)**: After your job completes, if the cache was updated or if no matching cache was found initially, the updated or new cache content from that mount point is saved under the specified key for future runs.

### Common Issues & Misconceptions

A frequent problem arises when the cache key isn't truly stable or predictable. For instance:

  * **Dynamic Cache Keys**: If your cache key is derived from the *"current Python version in the system,"* a common expectation is that the cache will be tied to that specific **version**. However, if your build process then changes the **Python version mid-workflow**, the cache identifier might effectively change. This means that at the end of the run, the cache might be saved under a different `ID` than what was expected at the beginning, leading to cache **misses** on subsequent runs.
  * **Ignoring Cache Keys**: Not carefully managing how cache keys are generated can result in caches that are never hit or are constantly invalidated, negating the performance benefits.

### Key Takeaways for Effective Caching

To leverage caching effectively and avoid these issues:

  * **Always Verify Cache Key Generation**: Explicitly understand and control how your cache ID (key) is generated. Ensure it's based on stable inputs that only change when you want the cache to invalidate (e.g., a hash of your `requirements.txt` or `pyproject.toml`, combined with the Python version you intend to use for the build).
  * **Monitor Cache Usage in GitHub UI**: Regularly check the GitHub Actions interface to confirm that your cache IDs and sizes match your expectations. This visual check can quickly reveal if your caches are being hit, if they're growing as anticipated, or if they're constantly being re-created due to invalid keys.


## Action Workflow Changes from build.yml

We've made significant updates to our GitHub Actions workflows, especially in how we manage dependencies and builds, moving away from the older `build.yml` structure.

### Key Improvements

  * **Efficient pyembroidery Handling**: We've removed `submodule: recursive` from all workflows. Instead, `pyembroidery` is now created as a Python package on the fly, streamlining its integration and reducing build overhead.
  * **uv-Exclusive Python Management**: All direct Python installations have been removed from workflows. `uv` now exclusively manages all Python installations and environments, simplifying setup and ensuring consistency.
  * **Simplified Release Job**: The release job is now much simpler. Everything found in the workflow artifacts is directly pushed to the release repository, making artifact management more straightforward.


### Linux32 Specific Fixes

  * **Corrected Volume Mount**: The volume mount for **linux32** was fixed from `${{ github.workspace }}:/__e/node20`. Using `github.workspace` is problematic because it's frequently overwritten by subsequent checkout actions or other commands.
  * **Custom Mount Point**: We now use a custom mount point (e.g., `my-node20-linux32:/__e/node20`) for reliable volume attachment.
  * **Node.js Issue on Linux32**: Note that GitHub's runners for **linux32** incorrectly mount the `node.js` version intended for **linux64**, which understandably won't run on a 32-bit processor. This fix addresses that specific problem.


### Backward Compatibility & Future Plans

  * For now, we've kept most other aspects of the workflows as unchanged as possible to maintain backward compatibility.


### Windows Signing: Release vs. Prerelease

* **A key question arises regarding Windows signing**: Why is there a distinction between release and prerelease signing for Windows? This is a critical point that would benefit from further clarification.


## To-Do & Future Improvements

Here's a concise overview of immediate action items and potential improvements for our build processes:

### GitHub Workflow & Variable Management

  * **GITHUB_REF Modernization**: The use of `GITHUB_REF` should be updated to `GITHUB_REF_NAME` for cleaner variable handling. Ideally, this should then be replaced by a more flexible input variable (like `input_tag`) to enable truly dynamic builds triggered by external scripts.

  * **Windows uv Signing**: We need to clarify why there's a distinction between release and pre-release signing for Windows builds. A simpler approach would be to sign all builds (releases and pre-releases) consistently, if feasible.

### Build Speed Optimizations

We can significantly accelerate build times, especially for Linux:

  * **Linux wxPython Wheels**: Currently, PyPI generally doesn't provide pre-built `wxPython` wheels for *Linux*, which greatly slows down InkStitch builds due to compilation. We should prepare custom `wxPython` packages for our target *Linux* distributions and store them in a permanent release repository. This would allow us to simply download them during builds instead of compiling.
  * **Existing Wheel Availability**: Pre-built .whl (wheel) packages for `wxPython` are readily available for *Windows* and *macOS*. While *linux64* also has wheels, their availability can be less standardized than on other platforms.



## GitHub Actions: Skipping Workflows

Just for your information:

You can easily skip GitHub Actions workflows for a specific commit by including `[no ci]` or `[skip ci]` (case-insensitive) in your commit message. https://docs.github.com/en/actions/managing-workflow-runs-and-deployments/managing-workflow-runs/skipping-workflow-runs

For example:
```Bash
git commit -m "My commit message [skip ci]"
```
This is handy for small changes like typos or documentation updates that don't require a full CI/CD run.



## Example: uv Initialization & Environment

Here's how to quickly get started with uv for your project:

  * `uv init` - Project Setup:
    * This command initializes your project and sets up key files:
        * `main.py` is removed (if created by default).
        * `.python-version` holds your selected Python version. We recommend ignoring this file in `.gitignore` so each user can prefer their own Python version.
        * `pyproject.toml` is created, serving as InkStitch's main project configuration.

  * `uv venv` - Virtual Environment Creation:
    * This command initializes your .venv (virtual environment) using the Python version specified in `.python-version` (e.g., Python 3.11).
    * Run `uv venv` any time you change your desired Python version in `.python-version` to recreate the environment accordingly.

