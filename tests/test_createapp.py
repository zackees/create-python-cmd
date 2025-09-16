"""
Test create app functionality.
"""

import os
import tempfile
from pathlib import Path

import pytest

from create_python_cmd.createapp import do_create_python_app


def read_utf8(path: str) -> str:
    """Read a file as UTF-8."""
    with open(path, encoding="utf-8") as file:
        return file.read()


@pytest.mark.integration
def test_create_python_app():
    """Test creating a complete Python app and running its tools."""
    with tempfile.TemporaryDirectory() as tmpdir:
        outdir = os.path.join(tmpdir, "my-app-test")

        # Create the app
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

        # Verify core files exist
        assert os.path.exists(outdir)
        assert os.path.exists(os.path.join(outdir, "pyproject.toml"))
        assert os.path.exists(os.path.join(outdir, "setup.py"))
        assert os.path.exists(os.path.join(outdir, "src", "my_app"))
        assert os.path.exists(os.path.join(outdir, "src", "my_app", "cli.py"))
        assert os.path.exists(os.path.join(outdir, "src", "my_app", "__init__.py"))
        assert os.path.exists(os.path.join(outdir, "tests"))
        assert os.path.exists(os.path.join(outdir, "tests", "test_cli.py"))
        assert os.path.exists(os.path.join(outdir, ".gitignore"))

        # Verify setup.py contains expected keywords
        setup_py_content = read_utf8(os.path.join(outdir, "setup.py"))
        assert 'KEYWORDS = "myapp test"' in setup_py_content


@pytest.mark.integration
def test_created_app_structure():
    """Test that created app has proper file structure."""
    with tempfile.TemporaryDirectory() as tmpdir:
        outdir = os.path.join(tmpdir, "test-structure")

        do_create_python_app(
            "test-app",
            app_description="Test description",
            app_author="Test Author",
            app_keywords="test keywords",
            version="0.1.0",
            github_url="https://github.com/test/test-app",
            command_name="test-app",
            cwd=outdir,
            chmod_scripts=False,
        )

        # Check that main source files exist
        src_dir = Path(outdir) / "src" / "test_app"
        assert src_dir.exists()
        assert (src_dir / "__init__.py").exists()
        assert (src_dir / "cli.py").exists()

        # Check that test directory exists
        tests_dir = Path(outdir) / "tests"
        assert tests_dir.exists()
        assert (tests_dir / "test_cli.py").exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
