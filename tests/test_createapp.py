"""
Unit test file.
"""
import os
import shutil
import subprocess
import unittest

from create_python_cmd.createapp import do_create_python_app

HERE = os.path.abspath(os.path.dirname(__file__))


def read_utf8(path: str) -> str:
    """Read a file as UTF-8."""
    with open(path, encoding="utf-8", mode="r") as file:
        return file.read()


class CreateAppTester(unittest.TestCase):
    """Main tester class."""

    def test_imports(self) -> None:
        """Test command line interface (CLI)."""

        outdir = os.path.normpath(os.path.join(HERE, "..", ".MyAppTest"))
        if os.path.exists(outdir):
            shutil.rmtree(outdir)
        do_create_python_app(
            app_description="MyAppTest description",
            app_author="Firstname Lastname",
            app_keywords="myapp test",
            version="1.2.3",
            github_url="https://github.com/author/my-app",
            command_name="mytestcommand",
            cwd=outdir,
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
        os.chdir(outdir)

        cmds = [
            "pip install -e .",
            "pip install -r requirements.testing.txt",
            "black src",
            "black tests",
            "python tests/test_cli.py",
            "pylint src tests",
            "flake8 src tests",
            "mypy src tests",
        ]
        assert os.path.exists(os.path.join(outdir, "lint"))
        env_with_current_dir = os.environ.copy()
        os_sep = ";" if os.name == "nt" else ":"
        env_with_current_dir["PATH"] = f"{outdir}{os_sep}{env_with_current_dir['PATH']}"
        for cmd in cmds:
            rtn = subprocess.call(cmd, env=env_with_current_dir, shell=True)
            self.assertEqual(0, rtn, f"Command failed: {cmd}")


if __name__ == "__main__":
    unittest.main()
