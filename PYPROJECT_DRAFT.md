

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

UV is the ideal choice for CI integration, offering blazing-fast dependency resolution, self-contained Rust architecture, direct Python version management, and streamlined caching, all of which significantly accelerate and simplify automated build processes across diverse environments.



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

    uv pip install my_debugger
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
  * **Format Differences**: The formats vary minimally (e.g., `numpy` in `requirements.txt` vs. `"numpy",` in `pyproject.toml`).
  * **uv Support**: `uv` supports installing from both file types:
    * `uv pip install -r requirements.txt` or
    * `uv pip install -r pyproject.toml`.



## General Rules `pyproject.toml`


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

  * **messages.po**:  This target was designed for localization (L10n), specifically for extracting translatable strings into `.po` files. Refer to the action at `.github/workflows/translations.yml` and [translate.inkstitch.org](http://translate.inkstitch.org) for details.



## GitHub Workflow Action Updates

We've significantly overhauled InkStitch GitHub Actions CI/CD system to streamline builds, improve maintainability, and reduce strain on GitHub resources.

### Build System Workflow

This document outlines the current workflow for building and signing distribution packages.

  * **Push Builds**:

    * Pushing changes to any branch (excluding release branches or tags) will only trigger tests. There is no reason to create distribution packages at this stage.

  * **On-Demand Package Compilation**:

    * Compilation of packages for a specific branch can be triggered manually via the [gh CLI](https://cli.github.com/).

    * This can be initiated for specific operating systems incrementally, or for all supported operating systems simultaneously.
    Refer to the script `bin/uv/gh_action_run.sh`.

  * **Release Build Trigger (Initial Stage)**:

    * A release build is triggered automatically by pushing a `v* tag` (e.g., `v1.0.0`).

    * Initially, this build will NOT include automatic signing or notarization. This is due to our current limitations regarding the automated signing process for Windows and notarization for macOS.

    * At this stage, the build will also not be marked as a '_release_' in the GitHub UI. This step is performed manually later.

  * **Authorized Signing and Notarization (Second Stage)**:

    * Once the packages from the initial release build have been verified (i.e., successfully installed and tested for functionality), a separate, subsequent build will be performed.

    * This build will be triggered manually via the `gh CLI`, with a specific `sign` nad `input_tag` parameters.

    * This particular build will include the necessary authorization for Windows signing and macOS notarization.

  * **Final Release Marking**:

    * After the signed/notarized packages are ready, the corresponding build will be manually marked as a formal release in the GitHub UI.

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


### Notes for Tag-Based Workflow Activation**:

The `uv_build.yml` workflow can also be activated by specific Git tags:

  * **vX.X.X***: Triggers a release build with `build_type=dummy`.
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



## Local GitHub Actions Testing with `act`

Testing GitHub Actions workflows can be slow and frustrating due to the need to push changes to GitHub and wait for runner execution. The `act` (https://github.com/nektos/act) tool, a single-file executable written in `Go`, allows you to run your GitHub Actions workflows locally, significantly speeding up development and debugging.


### Limitations of `act`

While act is an invaluable tool for local GitHub Actions development and debugging, it has some limitations:

* **Not a perfect replica**: It doesn't fully mimic the exact GitHub-hosted runner environment, leading to minor behavioral differences.
* **Partial context support**: Some github context variables (like github.event or github.token behavior) may be incomplete or require explicit mocking.
* **Limited runner types**: Primarily supports Linux jobs via Docker; native macOS/Windows runner simulation is not comprehensive.
* **Ignored workflow features**: Directives like concurrency, run-name, job.permissions, and timeout-minutes are often not respected.
* **No external artifact downloads**: Cannot fetch artifacts from other workflow runs or repositories.
* **Requires Docker**: Relies on Docker for environment simulation, meaning Docker must be installed and running.

### Usage `act` in Inkstitch

Here's how to use `act` for local testing of InkStitch workflows:

  * **Install act and add to PATH**: Download and install the act executable, then ensure its location is added to your system's `PATH` environment variable.

  * **Create Your Test Workflow**: Develop and refine your testing workflow (e.g., `test.yml`) within the `.github/workflows/` directory.

  * **Run act**: Execute your workflow using act, providing an input data file if your workflow expects inputs (like `uv_build.yml`).
    ```bash
    WF=.github/workflows/test.yml
    DAT=test.json
    act workflow_dispatch -W $WF  -e $DAT
    ```
    Here, `test.json` is the input data file. An example `test.json` matching the `uv_build.yml` inputs would look like this:
    ```json
    {
      "inputs": {
        "build_type": "linux64",
        "break_on": "sync"
      }
    }
    ```


## Testing Installation on different OS

* **Windows 10 (64-bit):**
  * **Passed**
  * **Note:** Sticking to `numpy<2.3` appears to resolve the previous issue.