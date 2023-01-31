"""Create a Python application."""


# pylint: disable=all
# flake8: noqa


import os
import tempfile
from shutil import which, rmtree


def check_name(app_name: str) -> None:
    """Check the name of the application."""
    if not app_name.isidentifier():
        raise ValueError("The name of the application is not a valid Python identifier.")


def check_semantic_version(version: str) -> None:
    """Check the version of the application."""
    version_list = version.split(".")
    for v in version_list:
        if not v.isnumeric():
            raise ValueError("The version of the application is not a valid semantic version.")


def do_create_python_app(
    app_name: str,
    app_description: str,
    app_author: str,
    version: str,
    github_url: str,
    add_commmand: bool,
) -> None:
    # Create the app directory
    os.makedirs(app_name, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmpdir:
        # download https://github.com/zackees/template-python-cmd
        # extract to tmpdir
        # copy files from tmpdir to app_name
        os.system(f"git clone https://github.com/zackees/template-python-cmd {tmpdir}")
        print(os.listdir(tmpdir))
        pyproject = os.path.join(tmpdir, "pyproject.toml")
        with open(pyproject, encoding="utf-8", mode="r") as pyproject_file:
            pyproject_lines = pyproject_file.readlines()
        for i, line in enumerate(pyproject_lines):
            if line.startswith("name ="):
                pyproject_lines[i] = f'name = "{app_name}"'
            if line.startswith("description ="):
                pyproject_lines[i] = f'description = "{app_description}"'
            if line.startswith("version ="):
                pyproject_lines[i] = f'version = "{version}"'
            if line.startswith("authors ="):
                pyproject_lines[i] = f'authors = ["{app_author}"]'
        with open(pyproject, encoding="utf-8", mode="w") as pyproject_file:
            pyproject_file.writelines(pyproject_lines)
        # change the url in setup.py
        setup = os.path.join(tmpdir, "setup.py")
        with open(setup, encoding="utf-8", mode="r") as setup_file:
            setup_lines = setup_file.readlines()
        for i, line in enumerate(setup_lines):
            if line.startswith("URL ="):
                setup_lines[i] = f'URL = "{github_url}"'
            # maintainer
            if line.startswith("maintainer="):
                setup_lines[i] = f'maintainer="{app_author}"'
        with open(setup, encoding="utf-8", mode="w") as setup_file:
            setup_file.writelines(setup_lines)
        # remove the .git directory
        rmtree(os.path.join(tmpdir, ".git"))


def create_python_app() -> None:
    """Create a Python application."""
    # check if git exists
    if not which("git"):
        raise RuntimeError("Git is not installed.")
    app_name = input("Python app name: ")
    check_name(app_name)
    app_description = input("Python app description: ")
    app_author = input("Python app author: ")
    github_url = input("GitHub URL: ")
    version = input("Version [1.0.0]: ")
    if not version:
        version = "1.0.0"
    check_semantic_version(version)
    add_command = input("Add a command? [y/N]: ")
    add_command = add_command.lower() == "y" or add_command == ""
    do_create_python_app(
        app_name=app_name,
        app_description=app_description,
        app_author=app_author,
        version=version,
        github_url=github_url,
        add_commmand=add_command,
    )


if __name__ == "__main__":
    create_python_app()
