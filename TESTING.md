# Testing Guide for Playbooks

## Overview

Playbooks includes a comprehensive test suite with:

- **19+ test cases** covering library and CLI functionality
- **80% code coverage requirement**
- **Python versions** (3.12)
- **Pre-commit hooks** for automated quality checks

## Running Tests Locally

### Quick Start

```bash
# Install dev dependencies
make dev

# Run all tests
make test

# Run specific test file
uv run pytest tests/test_library.py -v

# Run specific test
uv run pytest tests/test_library.py::TestPrompt::test_prompt_customize -v
```

### Test Coverage

```bash
# Generate coverage report (HTML)
uv run pytest tests/ --cov=src/playbooks --cov-report=html

# View HTML report
open htmlcov/index.html
```

## Test Structure

### test_library.py (10 tests)

Tests for the `PromptLibrary` core functionality:

```
TestPrompt (5 tests):
  ✓ test_prompt_creation - Create Prompt instances
  ✓ test_prompt_customize - Customize prompts with parameters
  ✓ test_prompt_quality_score - Retrieve quality scores
  ✓ test_prompt_production_tested - Check production flag
  ✓ test_prompt_test_count - Get test count

TestPromptLibrary (5 tests):
  ✓ test_library_creation - Initialize library
  ✓ test_library_list_prompts - List all prompts
  ✓ test_library_list_by_category - Filter by category
  ✓ test_library_get_prompt - Get specific prompt
  ✓ test_library_search - Search prompts
```

### test_cli.py (9 tests)

Tests for the CLI command-line interface:

```
TestCLI (9 tests):
  ✓ test_cli_help - Help command
  ✓ test_cli_version - Version command
  ✓ test_cli_list - List prompts
  ✓ test_cli_list_by_category - Filter by category
  ✓ test_cli_show - Show prompt details
  ✓ test_cli_search - Search functionality
  ✓ test_cli_search_no_results - Handle empty results
  ✓ test_cli_list_nonexistent_category - Error handling
  ✓ test_cli_show_nonexistent - Handle missing prompts
```

## Continuous Integration

### GitHub Actions (test.yml)

Automatically runs on:

- Push to `main` or `develop`
- Pull requests to `main` or `develop`

**Test Matrix:**

- Python 3.12
- Ubuntu latest

**Jobs:**

1. **Tests** - pytest with coverage
2. **Linting** - ruff checks and formatting
3. **Type Checking** - mypy validation
4. **Security** - bandit scanning

### Pre-commit Hooks

Automatically run before each commit:

```bash
# Install hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

**Hooks:**

- ruff: Linting and formatting
- trailing-whitespace: Remove trailing spaces
- end-of-file-fixer: Fix file endings
- check-yaml: Validate YAML syntax
- mypy: Type checking

## Writing New Tests

### Test Template

```python
import pytest
from playbooks import PromptLibrary

class TestNewFeature:
    """Test new feature."""

    def test_feature_behavior(self):
        """Test expected behavior."""
        library = PromptLibrary()
        result = library.some_method()

        assert result is not None
        assert isinstance(result, list)
```

### Naming Convention

- Test files: `test_*.py`
- Test classes: `Test*`
- Test methods: `test_*`

### Example: Testing a New Prompt

```python
def test_new_prompt_loaded(self):
    """Test new prompt is loaded and accessible."""
    library = PromptLibrary()
    prompt = library.get_prompt("category", "new_prompt")

    assert prompt is not None
    assert prompt.name == "Expected Name"
    assert len(prompt.inputs) > 0
    assert len(prompt.outputs) > 0
```

## Coverage Requirements

Minimum coverage: **80%**

When adding new code:

1. Write tests for new functionality
2. Ensure coverage doesn't drop below 80%
3. Check coverage report: `htmlcov/index.html`

```bash
# Check if coverage meets minimum
uv run pytest tests/ --cov=src/playbooks --cov-fail-under=80
```

## Debugging Tests

### Run with verbose output

```bash
uv run pytest tests/ -vv
```

### Run with print statements

```bash
uv run pytest tests/ -s
```

### Run single test with debugger

```bash
uv run pytest tests/test_library.py::TestPrompt::test_prompt_customize -vv -s
```

### Stop on first failure

```bash
uv run pytest tests/ -x
```

## Common Issues

### ImportError: No module named 'playbooks'

```bash
# Reinstall in editable mode
uv pip install -e .
```

### Tests not found

```bash
# Ensure you're in the right directory
cd /path/to/playbooks

# Verify pytest can find tests
uv run pytest --collect-only
```

### Coverage not meeting threshold

```bash
# See which lines aren't covered
uv run pytest tests/ --cov=src/playbooks --cov-report=html
open htmlcov/index.html
```

## Performance

Test execution time: **< 2 seconds**

```bash
time uv run pytest tests/
# Tests should complete in under 2 seconds
```

## Best Practices

1. **Keep tests focused** - One assertion per test when possible
2. **Use descriptive names** - Test names should explain what they test
3. **Don't test implementation** - Test behavior, not internals
4. **Use fixtures** - Reuse common setup with pytest fixtures
5. **Mock external calls** - Don't hit real APIs in tests
6. **Test edge cases** - Empty inputs, None values, invalid data

## CI/CD Integration

Tests automatically run on:

- Every push to `main`
- Every pull request
- Can be triggered manually

Results visible in:

- GitHub Actions tab
- PR checks
- Commit status

## Metrics

Current test suite:

- **19+ test cases**
- **Coverage: 80%+**
- **Execution time: <2s**
- **Python versions: 3.12**

## Further Reading

- [pytest documentation](https://docs.pytest.org/)
- [Python testing best practices](https://docs.python.org/3/library/unittest.html)
- [pre-commit documentation](https://pre-commit.com/)
