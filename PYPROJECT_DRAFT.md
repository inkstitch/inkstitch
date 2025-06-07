

# Proposal: Accelerating and Modernizing InkStitch Dependency Management with `uv` and `pyproject.toml`

This proposal outlines how to migrate InkStitch's Python dependency management to `uv` for faster, more reliable, and reproducible builds.

While there are indeed many excellent `Python` package managers out there (`Poetry`, `PDM`, `Hatch`, `Pipenv`, etc.), `uv` stands out primarily because of its unmatched speed.

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

Let's dive into how `uv` can be specifically applied to **InkStitch**, assuming the reader is already familiar with `uv`'s basics.

* **Instalation uv**: see https://github.com/astral-sh/uv
 and use direct download.

   * Linux, MacOS
   `curl -LsSf https://astral.sh/uv/install.sh | sh`
   * Windows `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`


* **Install tools**:
`uv tool install` command lets you install Python-based command-line utilities into isolated environments. This makes tools like linters (`Ruff`), build systems like `CMake`, or other utilities accessible from anywhere on your system without cluttering your global Python setup.
```
uv tool install --from git+https://github.com/karnigen/uvr uvr
uv tool install ruff
uv tool install flake8
uv tool install cmake

```
* **Use Worktree**: Worktrees are a neat Git feature that let you have multiple working directories, each with a different branch checked out, all sharing the same Git repository's history. Think of it as having several separate workspaces for one project without creating multiple full clones.

* **Creating a Git Worktree**
  * **Go to main repo**: `cd /path/to/your/inkstitch`
  * **Add new worktree**:
    *  *Existing branch*: `git worktree add ../new-dir existing-branch`
    *  *New branch*: `git worktree add ../new-dir -b new-branch`
    *  *Specific commit*: `git worktree add ../new-dir HEAD~3`
  * **Verify**: `git worktree list`

* Set **Python version** for **InkStitch**:
  * **Go to** your InkStitch main repo or worktree directory: `cd /path/to/your/inkstitch`
  * **List** available pythons: `uv python list`
  * **Set** python version: `uv python pin 311`
  * **Create** virtual environment (`.venv` directory): `uv venv`
  * **Install** local packages, using `uv pip` subsystem: Using `uv pip` does not modify `pyproject.toml`, avoid using `uv add` that modify `pyproject.toml` for everyone. `pyproject.toml` must be kept unified across all platforms and OS's.
    ```
    uv pip install my_package

    # prebuild wxpython for linux64
    uv pip install "https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-22.04/wxpython-4.2.3-cp311-cp311-linux_x86_64.whl"

    uv pip my_debugger
    ```
  * **Install** packages from `pyproject.toml`:
    ```
    uv sync --inexact
    ```
    Using `uv sync` without `--inexact` clears all `uv pip install` packages and let only thouse specified in `pyproject.toml`.


## ToDo
* **GITHUB_REF**: Should by replaced by `GITHUB_REF_NAME`, and this should be replaced by some variable to enable dynamic build from script.

* **Window64 signing**: Why there is release signing? Why not we simply sign all build?

## No action commit on github:
* commit message with **[no ci]** will skip action

## Remove `.gitmodules` & `pyembroidery` directory
* done
* *pyembroidery* will be added as library

## Keep `requirements.txt` for backward compatibility
* but pyproject.toml is not fully compatible
  * eg. relative dependency is not allowed in pyproject.toml
    * but **uv** support it
* both version must be maintained by hand

## uv
* `uv init` - initialize project and creates files
  * `main.py` - deleted
  * `.python-version` - contain selected python version
    * ignore in git (each user may prefer different version of python)
  * `pyproject.toml` - project for inkstitch

* `uv venv` - initialize .venv by python version as specified in `.python-version` (3.9)
  * run `uv venv` after each change of python version

## Packages not maintained by `pyproject.toml`
* use `uv pip install`  without explicitly telling `uv` to update based on pyproject.toml

## Adding libraries
* pyembroidery from inkstitch (latest version)
  * `pyembroidery @ git+https://github.com/inkstitch/pyembroidery`
  * `uv sync` or `uv sync -U` update packages
  * ignore `uv.lock` in `.gitignore` (depends on system used)

## activate virtual environment
* . .venv/bin.activate


