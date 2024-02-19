# create-python-cmd

[![Linting](https://github.com/zackees/createpythonapp/actions/workflows/lint.yml/badge.svg)](https://github.com/zackees/createpythonapp/actions/workflows/lint.yml)

[![MacOS_Tests](https://github.com/zackees/createpythonapp/actions/workflows/push_macos.yml/badge.svg)](https://github.com/zackees/createpythonapp/actions/workflows/push_macos.yml)
[![Ubuntu_Tests](https://github.com/zackees/createpythonapp/actions/workflows/push_ubuntu.yml/badge.svg)](https://github.com/zackees/createpythonapp/actions/workflows/push_ubuntu.yml)
[![Win_Tests](https://github.com/zackees/createpythonapp/actions/workflows/push_win.yml/badge.svg)](https://github.com/zackees/createpythonapp/actions/workflows/push_win.yml)

```python
> pip install create-python-cmd
> git clone https://github.com/.../myproject
> cd myproject
> createpythoncmd # Creates a new Python command line application.
```

Creates a new Python command line application with linters and tests.

# Linters

The following linters are used
  * `pylint`
  * `flake8`
  * `mypy`

# Testing

To run all linters and tests, simply go to the root directory and run `tox`

# Uploading your project to PYPI

To upload your project to pypi simply run `. ./upload_package.sh`

# Versions
  * `1.2.2` - Adds retries to get correct parameters and auto corrects parameters instead of exiting.
  * `1.2.0` - Refresh with new modern practices like an installation script.
  * `1.1.1` - Adds chmod +x to shell scripts and adds post install instructions.
  * `1.1.0` - createpythonapp -> createpythoncmd.
  * `1.0.9` - Adds keywords prompt during setup.