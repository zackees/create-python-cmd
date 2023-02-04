"""Create a Python application."""


# pylint: disable=all
# flake8: noqa


import os
import tempfile
import shutil
from typing import Optional


def check_name(app_name: str) -> None:
    """Check the name of the application."""
    if not app_name.isidentifier():
        raise ValueError(
            "The name of the application is not a valid Python identifier."
        )


def check_semantic_version(version: str) -> None:
    """Check the version of the application."""
    version_list = version.split(".")
    for v in version_list:
        if not v.isnumeric():
            raise ValueError(
                "The version of the application is not a valid semantic version."
            )


def remove_double_blank_lines(lines: list) -> list:
    """Remove double blank lines."""
    new_lines = []
    last_line_blank = False
    for i, line in enumerate(lines):
        if line == "":
            if last_line_blank:
                continue
            new_lines.append(line)
            last_line_blank = True
        else:
            new_lines.append(line)
            last_line_blank = False
    return new_lines


def do_create_python_app(
    app_description: str,
    app_author: str,
    version: str,
    github_url: str,
    command_name: Optional[str] = None,
    cwd: Optional[str] = None,
) -> None:
    # Create the app directory
    # get app name from the github url
    cwd = cwd or os.getcwd()
    os.makedirs(cwd, exist_ok=True)
    app_name = github_url.split("/")[-1]
    app_name_underscore = app_name.replace("-", "_")
    with tempfile.TemporaryDirectory() as tmpdir:
        # download https://github.com/zackees/template-python-cmd
        # extract to tmpdir
        # copy files from tmpdir to app_name
        os.system(f"git clone https://github.com/zackees/template-python-cmd {tmpdir}")
        # change every directory name of from template-python-cmd to app_name
        for root, dirs, files in os.walk(tmpdir):
            for d in dirs:
                if d == "template-python-cmd" or d == "template_python_cmd":
                    shutil.move(
                        os.path.join(root, d), os.path.join(root, app_name_underscore)
                    )
        pyproject = os.path.join(tmpdir, "pyproject.toml")
        with open(pyproject, encoding="utf-8", mode="r") as pyproject_file:
            pyproject_lines = pyproject_file.read().splitlines()
        for i, line in enumerate(pyproject_lines):
            if line.startswith("name ="):
                pyproject_lines[i] = f'name = "{app_name}"'
            if line.startswith("description ="):
                pyproject_lines[i] = f'description = "{app_description}"'
            if line.startswith("version ="):
                pyproject_lines[i] = f'version = "{version}"'
            if line.startswith("authors ="):
                pyproject_lines[i] = f'authors = ["{app_author}"]'
            if command_name is None:
                if line.startswith("[project.scripts]"):
                    pyproject_lines[i] = ""
                if line.startswith("test_cmd ="):
                    pyproject_lines[i] = ""
            else:
                if line.startswith("test_cmd ="):
                    pyproject_lines[
                        i
                    ] = f'{command_name} = "{app_name_underscore}.cli:main"'
        pyproject_lines = remove_double_blank_lines(pyproject_lines)
        with open(pyproject, encoding="utf-8", mode="w") as pyproject_file:
            pyproject_file.write("\n".join(pyproject_lines))
        test_cli = os.path.join(tmpdir, "tests", "test_cli.py")
        with open(test_cli, encoding="utf-8", mode="r") as test_file:
            test_lines = test_file.read().splitlines()
        for i, line in enumerate(test_lines):
            if line.startswith('COMMAND = "test_cmd"'):
                new_line = f'COMMAND = "{command_name}"'
                test_lines[i] = new_line
        with open(test_cli, encoding="utf-8", mode="w") as test_file:
            test_file.write("\n".join(test_lines))
        # change the url in setup.py
        setup = os.path.join(tmpdir, "setup.py")
        with open(setup, encoding="utf-8", mode="r") as setup_file:
            setup_lines = setup_file.read().splitlines()
        for i, line in enumerate(setup_lines):
            if line.startswith("URL ="):
                setup_lines[i] = f'URL = "{github_url}"'
            # maintainer
            if line.startswith("maintainer="):
                setup_lines[i] = f'maintainer="{app_author}"'
        with open(setup, encoding="utf-8", mode="w") as setup_file:
            setup_file.write("\n".join(setup_lines))
        files = os.listdir(tmpdir)
        files = [os.path.join(tmpdir, f) for f in files if f != ".git"]
        for f in files:
            if os.path.isdir(f):
                shutil.copytree(f, os.path.join(cwd, os.path.basename(f)))
            else:
                shutil.copy(f, cwd)


def create_python_app() -> None:
    """Create a Python application."""
    # check if git exists
    if not shutil.which("git"):
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
    add_command = input("Add a command? [y/N]: ").lower() == "y"
    command_name = None
    if add_command:
        command_name = input("Command name: ")
        check_name(command_name)
    do_create_python_app(
        app_description=app_description,
        app_author=app_author,
        version=version,
        github_url=github_url,
        command_name=command_name,
    )


if __name__ == "__main__":
    create_python_app()