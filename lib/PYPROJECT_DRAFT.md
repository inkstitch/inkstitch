

# Alternative *pyproject*.toml and *uv* Project Manager Configurations

Here, we will document the process for setting up alternative configurations for ***pyproject.toml*** and leveraging the ***uv*** project manager.

## Resources
* pyproject.toml definition
  * https://packaging.python.org/en/latest/specifications/pyproject-toml/
* Dependency specifiers
  * https://packaging.python.org/en/latest/specifications/dependency-specifiers/

* **uv** project manager
  * https://github.com/astral-sh/uv

## No action commit on github:
* commit message with **[no ci]** will skip action

## Remove .gitmodules & pyembroidery directory
* done
* *pyembroidery* will be added as library

## Keep requirements for backward compatibility
* but pyproject.toml is not fully compatible
  * eg. relative dependency is not allowed in pyproject.toml
    * but **uv** support it
* both version must be maintained by hand

# uv
* `uv init` - initialize project and creates files
  * `main.py` - deleted
  * `.python-version` - contain selected python version
    * ignore in git (each user may prefer different version of python)
  * `pyproject.toml` - project for inkstitch

## TODO
* pyembroidery will be added as library into project
  * done

