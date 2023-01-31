"""
Unit test file.
"""
import os
import unittest
import shutil
import subprocess

from create_python_cmd.createapp import do_create_python_app

HERE = os.path.abspath(os.path.dirname(__file__))


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
            version="1.2.3",
            github_url="https://github.com/author/my-app",
            command_name="mytestcommand",
            cwd=outdir,
        )
        self.assertTrue(os.path.exists(outdir))
        self.assertTrue(os.path.exists(os.path.join(outdir, "pyproject.toml")))
        self.assertTrue(os.path.exists(os.path.join(outdir, "setup.py")))
        self.assertTrue(os.path.exists(os.path.join(outdir, "src", "my_app")))
        self.assertTrue(os.path.exists(os.path.join(outdir, "src", "my_app", "cli.py")))
        self.assertTrue(os.path.exists(os.path.join(outdir, "src", "my_app", "__init__.py")))
        self.assertTrue(os.path.exists(os.path.join(outdir, "tests")))
        self.assertTrue(os.path.exists(os.path.join(outdir, "tests", "test_cli.py")))
        # tox
        self.assertTrue(os.path.exists(os.path.join(outdir, "tox.ini")))
        os.chdir(outdir)
        # rtn = os.system("tox")
        subprocess.check_call("pip install -e .", shell=True)
        subprocess.check_call("python tests/test_cli.py", shell=True)
        subprocess.check_call("pylint src tests", shell=True)
        subprocess.check_call("flake8 src tests", shell=True)
        subprocess.check_call("mypy src tests", shell=True)
        # self.assertEqual(rtn, 0)


if __name__ == "__main__":
    unittest.main()
