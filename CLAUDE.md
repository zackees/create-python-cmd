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