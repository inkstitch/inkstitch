# Setup/Build Instructions for Developers

## Linux/macOS

**Install `uv` & Set Up Environment**:

  * **`uv`** - Python package and project manager

      * Homepage: [https://github.com/astral-sh/uv](https://github.com/astral-sh/uv)
      * Install: `curl -LsSf https://astral.sh/uv/install.sh | sh`

  * **`uvr`** - Run scripts in a virtual environment

      * Homepage: [https://github.com/karnigen/uvr](https://github.com/karnigen/uvr)
      * Install: `uv tool install --from git+https://github.com/karnigen/uvr uvr`
      * Ensure `uvr` is on your **PATH** (`~/.local/bin` is a common location).

  * **`make`** - Build tool, usually pre-installed on Linux and macOS. If missing, install:

      * On Ubuntu/Debian: `sudo apt-get install make`
      * On Fedora: `sudo dnf install make`
      * On Arch Linux: `sudo pacman -S make`
      * On macOS (with Homebrew): `brew install make`

**Install Inkscape**

  * See [https://inkscape.org/release](https://inkscape.org/release) for installation options.
  * For Ubuntu/Debian, a PPA is available: [https://launchpad.net/\~inkscape.dev/+archive/ubuntu/stable](https://launchpad.net/~inkscape.dev/+archive/ubuntu/stable)
  * Refer to their website for other distribution-specific instructions.

**Install Ink/Stitch**

  * Choose a working directory for Ink/Stitch (e.g., `/home/$USER/inkstitch_git`).

    ```bash
    git clone https://github.com/inkstitch/inkstitch.git
    cd inkstitch
    git worktree add ../my_dir branch_name
    cd ../my_dir
    ```

  * **Set up Ink/Stitch (from `my_dir`):**
    ```bash
    # Edit uv_setup.sh
    cp uv_setup_template.sh uv_setup.sh
    ./uv_setup.sh
    # Create .inx files (automatically calls uv_setup.sh if needed)
    make inx
    ```

  * **Activate Ink/Stitch in Inkscape (create symlink to .inx files):**

    ```bash
    cd ~/.config/inkscape/extensions
    ln -s ~/inkstitch_git/my_dir
    ```

    **Note:** Currently there is no need to use `python-interpreter="/path/to/python"` in `preferences.xml`, because we are using virtual Python environment.

-----

## Windows

These instructions assume you're using **Chocolatey** as your package manager, **git for Windows**, the **MSYS2** Unix-like subsystem with the **UCRT64** environment, and **uv** for Python package management.

**MSYS2** is a building tool for native Windows applications using GNU tools, replacing previous MSYS, MinGW, and Clang environments.

  * **Chocolatey (choco)** - Package manager

      * Homepage: [https://chocolatey.org/](https://chocolatey.org/)
      * Install: `Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))`
      * **Note:** Always use **Admin PowerShell** to install packages with `choco`.

  * **Multi Commander**

      * Homepage: [https://multicommander.com/](https://multicommander.com/)
      * This is optional but greatly simplifies creating symlinks.
      * Install: `choco install multicommander`

  * **`uv`** - Python package and project manager

      * Homepage: [https://github.com/astral-sh/uv](https://github.com/astral-sh/uv)
      * Install: `choco install uv`

  * **`uvr`** - Run scripts in a virtual environment

      * Homepage: [https://github.com/karnigen/uvr](https://github.com/karnigen/uvr)
      * Install: `uv tool install --from git+https://github.com/karnigen/uvr uvr`

  * **Git**

      * Homepage: [https://gitforwindows.org](https://gitforwindows.org)
      * Install: `choco install git`
      * **Note:** It's best to avoid the Git client provided by MSYS2 due to its ongoing integration challenges with Windows.

  * **MSYS2**

      * Homepage: [https://www.msys2.org/](https://www.msys2.org/)
      * Install: `choco install msys2` (This will install it to `C:\tools\msys64` by default.)
      * Uninstall: `choco uninstall msys2`
          * **Be careful when linking or creating a junction to your directories within the MSYS2 subsystem**, as uninstalling MSYS2 may recursively delete them.

  * **Inkscape**

      * Install: `choco install inkscape`

  * **Ink/Stitch**

      * Select your Ink/Stitch working directory (e.g., `C:\Users\%USERNAME%\Documents\inkstitch_git`).
      * Run `cmd.exe`:
        ```bash
        git clone https://github.com/inkstitch/inkstitch.git
        cd inkstitch

        # Check out your branch
        git worktree add ../my_dir branch_name
        cd ../my_dir
        ```

### UCRT64 Environment Setup

  * Create a directory `C:\MyScripts` for your Windows scripts.
  * **Create a symlink** from `C:\Users\%USERNAME%\Documents\inkstitch_git\my_dir\bin\msys2\ucrt.bat` to `C:\MyScripts\ucrt.bat`.
      * From an **Admin CMD** prompt: `mklink "C:\MyScripts\ucrt.bat" "C:\Users\%USERNAME%\Documents\inkstitch_git\my_dir\bin\msys2\ucrt.bat"`
      * Alternatively, use **Multi Commander**: `Tools` -\> `File Links` -\> `Create Links` -\> `Symlink`.
  * Update your registry using the file `bin/msys2/ucrt.reg` from your Ink/Stitch directory.
  * Optionally you can also symlink `pw.bat` as alias for **Powershell**.
  * Optionally enable UCRT64 bash in VS Code editor ( see `bin/msys2/vscode_setting.md`)

### Set Up PATHs

  * **Windows PATH** (for `cmd.exe` and `PowerShell`):

      * Edit your system's `PATH` environment variable to include these directories:
          * `C:\MyScripts` (for `ucrt.bat`, `pw.bat`)
          * `C:\ProgramData\chocolatey\bin` (for `choco`, `uv`)
          * `C:\Program Files\Git\cmd` (for `git`)
          * `C:\Users\%USERNAME%\.local\bin` (for `uvr`)
          * `C:\tools\msys64\usr\bin` (for `bash`, `make`, etc.)
          * `C:\Program Files\Inkscape\bin` (for `inkscape.com`)

  * **MSYS2 Subsystem PATH** (`C:\tools\msys64\home\$USER\.bashrc`):

      * Add these lines to your `.bashrc` file:
        ```bash
        export PATH="/c/Program Files/Git/cmd:$PATH"
        export PATH="/c/ProgramData/chocolatey/bin:$PATH"
        export PATH="/c/Users/$USER/.local/bin:$PATH"
        ```
        **Note:** Be aware that uninstalling MSYS2 will remove any custom configurations in bashrc.

### Install `make` within MSYS2

  * Activate the **UCRT64** environment by running `ucrt`.
  * Check if `UCRT64` is active: `echo $MSYSTEM` should output `UCRT64`.
  * Install **`make`** within `msys2` using Pacman:
    * `pacman -S make`
  * **Note:** For better compatibility and security, it's recommended to avoid old or unmaintained Windows versions of make.

### Activate Ink/Stitch in Inkscape

  * Within the **UCRT64** environment, navigate to your Ink/Stitch directory.

  * Run `ucrt`, then execute these commands:

    ```bash
    # Edit uv_setup.sh
    cp uv_setup_template.sh uv_setup.sh
    ./uv_setup.sh
    # Create .inx files (automatically calls uv_setup.sh if needed)
    make inx
    ```

  * From `C:\Users\%USERNAME%\AppData\Roaming\inkscape\extensions`:

      * As **administrator**, run `cmd.exe` and create a symbolic link:
          * `mklink /D C:\Users\%USERNAME%\AppData\Roaming\inkscape\extensions\my_dir C:\Users\%USERNAME%\Documents\inkstitch_git\my_dir`
      * Alternatively, use **Multi Commander**: `Tools` -\> `File Links` -\> `Create Links` -\> `Symlink`.

    **Note:** Currently there is no need to use `python-interpreter="/path/to/python"` in `preferences.xml`, because we are using virtual Python environment.

  * For developer-level execution of **Inkscape**, open PowerShell (see `pw.bat` for setup). Use `inkscape.com your.svg` specifically to capture and view **Inkscape's** console output, as `inkscape.exe` may not display it.

### Periodically Update Subsystems

  * **Chocolatey packages:**

      * Run **Admin PowerShell**.
      * `choco upgrade all -y`

  * **MSYS2 packages:**

      * Run `ucrt`.
      * `pacman -Syu` (**Note:** The order `-Syu` is important for proper synchronization and upgrade.)

  * **`uv` tools:**

      * Run `cmd.exe`.
      * `uv tool upgrade --all`



---

# Offline Debugging

You can activate offline debugging across all systems (Linux, macOS, and Windows).

**Steps:**

* Copy `DEBUG_template.toml` to `DEBUG.toml`, if you haven't already.
* Enable `create_bash_script = true` in `DEBUG.toml`.
    * Once you finish any InkStitch extension command in Inkscape, it will create a `debug_inkstitch.sh` script in the InkStitch working directory.
    * When you execute `debug_inkstitch.sh`:
        * First, the entire environment will be restored to match how Inkscape runs the command.
        * Next, the Python virtual environment will be activated.
        * Finally, `inkstitch.py` will execute with all its original arguments.
        * **Note:** On Windows, run `debug_inkstitch.sh` from the UCRT64 environment (use `ucrt`).

* **Debugger Preparation:**
    * Select your debugger's `debug_type` in `DEBUG.toml`.
    * Enable debugging by setting `debug_enable` to `true` or by using the `-d` argument for `debug_inkstitch.sh` (otherwise, `debug_type` will be `None`).

* **For Interactive Debugging (e.g., PyCharm, PyDev):**
    * Activate the **Python virtual environment**.
        * If your debugger doesn't support direct virtual environment activation, set the path to the Python interpreter directly.
        * **Important Note:** Activating a virtual environment simply prepends the path to your Python interpreter (within the virtual environment) to your system's `PATH` variable (e.g., `activate` == `/your/python_path:$PATH`). A direct call to `/your/python_path/python` achieves the same effect as running Python with a modified `PATH`, ensuring your desired Python is found first.
    * Set up all environment variables (copy them from `debug_inkstitch.sh` to your debugger's configuration).
    * Run your interactive debugger.

* **For Attached Debugging (e.g., VS Code):** This method is much simpler.
    * Just run `debug_inkstitch.sh`.
    * Attach to the script using your debugger (see `lib/debug/debugger.py` for how to set up remote debugging in VS Code).

---

