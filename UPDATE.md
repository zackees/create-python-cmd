task - modernize create-python-cmd

codeup is the premier fixup from the create-python-cmd template for repo creation

https://github.com/zackees/codeup

The improvements in the pyproject.toml, dropping flake8, pylint, mypy, and just using ruff, pyright is the way to go.

These improvements need to be merged back to this repo (create-python-cmd)


Important to note is the CLAUDE.md rules. Migrate these rules to ours.


## Next step

You need to update the unit tests.

Remember - NO MOCKS!

Audit the previous tests and see if they no longer make sense. If so delete them, you can be aggressive in this because now we have ai to remake the tests.

what also needs to be fixed up is the readme.md badges for linting and testing. we can't use relative paths anymore. So just get rid of them.


## Investigation Findings

### Current State Analysis
1. **Dependencies**: The current pyproject.toml has mixed tooling - it includes both ruff and mypy, while codeup has streamlined to just ruff and pyright for linting/type checking.

2. **Testing Dependencies**: Currently lists pytest but missing key testing packages that codeup uses:
   - pytest-xdist (parallel test execution)
   - pytest-timeout (prevent hanging tests)
   - pytest-cov (coverage reporting)

3. **Tool Configurations**: No ruff or pyright configurations present in pyproject.toml, while codeup has comprehensive settings for both.

4. **CLAUDE.md Rules**: Codeup emphasizes:
   - UV for environment management
   - KeyboardInterrupt handling prioritization
   - Dataclass usage over tuples
   - Test file standalone execution capability
   - Comprehensive exception logging

5. **README Badges**: Current badges point to old repository (zackees/createpythonapp) and need removal as suggested.

### Modernization Action Items
1. **Update pyproject.toml**:
   - Remove mypy, keep ruff and pyright only
   - Add missing test dependencies (pytest-xdist, pytest-timeout, pytest-cov)
   - Add [tool.ruff] and [tool.pyright] configuration sections from codeup
   - Update Python version requirement to >=3.8

2. **Create CLAUDE.md**:
   - Adapt codeup's CLAUDE.md for this project
   - Include linting commands: `ruff check .`, `pyright`
   - Specify test execution: `pytest` with no mocks policy
   - Add project-specific development guidelines

3. **Test Refactoring**:
   - Audit test_cli.py and test_createapp.py for relevance
   - Remove mock-based tests per directive
   - Ensure tests can run standalone with `if __name__ == "__main__"`
   - Add test markers for organization

4. **Documentation Cleanup**:
   - Remove all badges from README.md
   - Update any references to old tooling (flake8, pylint, mypy)


## Code Snippets for Proposed Changes

### 1. Updated pyproject.toml

```toml
[build-system]
requires = ["setuptools", "setuptools-scm"]
build-backend = "setuptools.build_meta"

[project]
name = "create-python-cmd"
description = "Cross platform(ish) productivity commands written in python."
requires-python = ">=3.8"
readme = "README.md"
keywords = ["create python cmd"]
license = { text = "BSD 3-Clause License" }
classifiers = ["Programming Language :: Python :: 3"]
dependencies = [
    "ruff",
    "pyright",
    "black",
    "pytest",
    "pytest-xdist",
    "pytest-timeout",
    "pytest-cov",
]
version = "2.0.1"

[project.scripts]
createpythoncmd = "create_python_cmd.cli:main"
create-python-cmd = "create_python_cmd.cli:main"

[tool.ruff]
line-length = 88
target-version = "py38"
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "UP",  # pyupgrade
]
ignore = [
    "E501", # line too long (handled by black)
]

[tool.pyright]
include = ["src", "tests"]
pythonVersion = "3.8"
typeCheckingMode = "basic"
reportMissingImports = true
```

### 2. CLAUDE.md Template

```markdown
# Claude Code Development Guidelines

## Project Overview
create-python-cmd - Cross platform productivity commands written in Python

## Development Environment
- Python 3.8+ required
- Use virtual environment for development
- Run commands from project root

## Linting and Type Checking
- Linting: `ruff check .`
- Formatting: `black .`
- Type checking: `pyright`

Always run these before committing changes.

## Testing Requirements
- Framework: pytest
- Run tests: `pytest`
- Parallel execution: `pytest -n auto`
- With coverage: `pytest --cov=src/create_python_cmd`

**IMPORTANT: NO MOCKS IN TESTS**
- Write integration tests that test actual functionality
- Use temporary directories for file operations
- Test real command execution

## Code Standards
1. **Exception Handling**
   - Always handle KeyboardInterrupt first
   - Log errors before handling
   - Use specific exception types

2. **Return Values**
   - Use dataclasses instead of tuples
   - Type all function returns

3. **File Structure**
   - All code in src/create_python_cmd/
   - Tests in tests/ with test_ prefix
   - Make test files executable standalone

## Example Test Structure

```python
import pytest
import tempfile
import os
from pathlib import Path

@pytest.mark.unit
def test_real_functionality():
    """Test actual functionality without mocks."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Perform real operations
        result = actual_function(tmpdir)
        assert result == expected

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```
```

### 3. Refactored Test Example (tests/test_cli.py)

```python
"""
Test command line interface functionality.
"""
import pytest
import subprocess
import sys
from pathlib import Path

@pytest.mark.unit
def test_cli_help():
    """Test that CLI help works."""
    result = subprocess.run(
        [sys.executable, "-m", "create_python_cmd", "--help"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "create-python-cmd" in result.stdout.lower() or "usage" in result.stdout.lower()

@pytest.mark.unit
def test_cli_version():
    """Test version display."""
    result = subprocess.run(
        ["createpythoncmd", "--version"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "2.0" in result.stdout

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

### 4. GitHub Actions Update (.github/workflows/test.yml)

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ["3.8", "3.9", "3.10", "3.11", "3.12"]

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e ".[dev]"

    - name: Lint with ruff
      run: ruff check .

    - name: Type check with pyright
      run: pyright

    - name: Run tests
      run: pytest -v --cov=src/create_python_cmd

```

### 5. Remove Badges from README.md

In README.md, remove these lines:
```markdown
[![Linting](https://github.com/zackees/createpythonapp/actions/workflows/lint.yml/badge.svg)](https://github.com/zackees/createpythonapp/actions/workflows/lint.yml)
[![MacOS_Tests](https://github.com/zackees/createpythonapp/actions/workflows/push_macos.yml/badge.svg)](https://github.com/zackees/createpythonapp/actions/workflows/push_macos.yml)
[![Ubuntu_Tests](https://github.com/zackees/createpythonapp/actions/workflows/push_ubuntu.yml/badge.svg)](https://github.com/zackees/createpythonapp/actions/workflows/push_ubuntu.yml)
[![Win_Tests](https://github.com/zackees/createpythonapp/actions/workflows/push_win.yml/badge.svg)](https://github.com/zackees/createpythonapp/actions/workflows/push_win.yml)
```

### 6. Updated requirements.testing.txt

```
pytest>=7.0.0
pytest-xdist>=3.0.0
pytest-timeout>=2.1.0
pytest-cov>=4.0.0
pyright>=1.1.0
ruff>=0.1.0
black>=23.0.0
```