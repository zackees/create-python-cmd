# create-python-cmd

[![Linting](https://github.com/zackees/createpythonapp/actions/workflows/lint.yml/badge.svg)](https://github.com/zackees/createpythonapp/actions/workflows/lint.yml)

[![MacOS_Tests](https://github.com/zackees/createpythonapp/actions/workflows/push_macos.yml/badge.svg)](https://github.com/zackees/createpythonapp/actions/workflows/push_macos.yml)
[![Ubuntu_Tests](https://github.com/zackees/createpythonapp/actions/workflows/push_ubuntu.yml/badge.svg)](https://github.com/zackees/createpythonapp/actions/workflows/push_ubuntu.yml)
[![Win_Tests](https://github.com/zackees/createpythonapp/actions/workflows/push_win.yml/badge.svg)](https://github.com/zackees/createpythonapp/actions/workflows/push_win.yml)


This is a command for creating a skeleton project for python commands. It uses
uv to boot strap the project and install an environment. Helpful utilities for
installing the project are given, wee below.

Template that this uses is here:
  * https://github.com/zackees/template-python-cmd

```python
> pip install create-python-cmd
> git clone https://github.com/.../myproject
> cd myproject
> createpythoncmd # Creates a new Python command line application.
```

Creates a new Python command line application with linters and tests.

# Tools

The following tools will be installed
  * `install` - script to boot strap and install the python package
  * `clean` - removes build artifacts
  * `lint` - runs the linters on the source code
  * `test` - runs the unit test

# Linters

The following linters are used
  * `ruff`
  * `black`
  * `isort`
  * `mypy`


# Uploading your project to PYPI

To upload your project to pypi simply run `. ./upload_package.sh`

# Versions
  * `2.0.0` - Moved to the uv build system as this is much better and fixes the boot strapping of python issue. Fixes git bash not being cd'd to the current directory in VSCode.
  * `1.2.5` - Varius fixes and test fixes.
  * `1.2.2` - Adds retries to get correct parameters and auto corrects parameters instead of exiting.
  * `1.2.0` - Refresh with new modern practices like an installation script.
  * `1.1.1` - Adds chmod +x to shell scripts and adds post install instructions.
  * `1.1.0` - createpythonapp -> createpythoncmd.
  * `1.0.9` - Adds keywords prompt during setup.