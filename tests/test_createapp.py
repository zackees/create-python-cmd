"""
Unit test file.
"""

import atexit
import os
import shutil
import subprocess
import unittest

from create_python_cmd.createapp import do_create_python_app

HERE = os.path.abspath(os.path.dirname(__file__))
REMOVE_AFTER_TEST = False


def read_utf8(path: str) -> str:
    """Read a file as UTF-8."""
    with open(path, encoding="utf-8", mode="r") as file:
        return file.read()


OUTDIR = os.path.normpath(os.path.join(HERE, "..", ".MyAppTest"))
if REMOVE_AFTER_TEST:
    atexit.register(lambda: shutil.rmtree(OUTDIR, ignore_errors=True))


class CreateAppTester(unittest.TestCase):
    """Main tester class."""

    def test_imports(self) -> None:
        """Test command line interface (CLI)."""

        outdir = OUTDIR
        if os.path.exists(outdir):
            shutil.rmtree(outdir)
        do_create_python_app(
            "my-app",
            app_description="MyAppTest description",
            app_author="Firstname Lastname",
            app_keywords="myapp test",
            version="1.2.3",
            github_url="https://github.com/author/my-app",
            command_name="my-app",
            cwd=outdir,
            chmod_scripts=False,
        )
        self.assertTrue(os.path.exists(outdir))
        self.assertTrue(os.path.exists(os.path.join(outdir, "pyproject.toml")))
        self.assertTrue(os.path.exists(os.path.join(outdir, "setup.py")))
        setup_py_lines: list[str] = read_utf8(
            os.path.join(outdir, "setup.py")
        ).splitlines()
        self.assertIn('KEYWORDS = "myapp test"', setup_py_lines)
        self.assertTrue(os.path.exists(os.path.join(outdir, "src", "my_app")))
        self.assertTrue(os.path.exists(os.path.join(outdir, "src", "my_app", "cli.py")))
        self.assertTrue(
            os.path.exists(os.path.join(outdir, "src", "my_app", "__init__.py"))
        )
        self.assertTrue(os.path.exists(os.path.join(outdir, "tests")))
        self.assertTrue(os.path.exists(os.path.join(outdir, "tests", "test_cli.py")))
        self.assertTrue(os.path.exists(os.path.join(outdir, "tox.ini")))
        self.assertTrue(os.path.exists(os.path.join(outdir, ".gitignore")))
        os.chdir(outdir)

        cmds = [
            "bash install",
            "uv pip install -r requirements.testing.txt",
            "black src",
            "black tests",
            "bash lint",
            "bash test",
        ]
        assert os.path.exists(os.path.join(outdir, "lint"))
        env_with_current_dir = os.environ.copy()
        env_with_current_dir.pop("IN_ACTIVATED_ENV", None)
        for cmd in cmds:
            print(f"Running command: {cmd} in {outdir}")
            rtn = subprocess.call(cmd, env=env_with_current_dir, shell=True, cwd=outdir)
            self.assertEqual(0, rtn, f"Command failed: {cmd}")


if __name__ == "__main__":
    unittest.main()
