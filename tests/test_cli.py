"""
Test command line interface functionality.
"""

import subprocess

import pytest


@pytest.mark.unit
def test_cli_help():
    """Test that CLI help works."""
    result = subprocess.run(
        ["createpythoncmd", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert (
        "createpythoncmd" in result.stdout.lower() or "usage" in result.stdout.lower()
    )


@pytest.mark.unit
def test_cli_command_exists():
    """Test that createpythoncmd command exists."""
    result = subprocess.run(
        ["createpythoncmd", "--help"], capture_output=True, text=True
    )
    assert result.returncode == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
