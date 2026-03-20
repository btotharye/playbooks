# Development Setup for Playbooks

## Prerequisites

- Python 3.11+
- `uv` (fast Python package installer)
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

## Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/btotharye/playbooks.git
cd playbooks
```

### 2. Install with uv
```bash
# Install package + dependencies
make dev

# Or manually:
uv pip install -e ".[dev]"
```

### 3. Run CLI
```bash
# List all prompts
playbooks list

# Show a specific prompt
playbooks show deployment-canary-001

# Search
playbooks search "cost"
```

## Development Workflow

### Run Tests
```bash
make test
# Or: uv run pytest tests/ -v
```

### Lint & Format
```bash
make lint      # Check code quality
make format    # Auto-format code
```

### Add a New Prompt

1. Create `prompts/{category}/{name}.yaml`
2. Follow format from existing prompts
3. Include metadata, inputs, outputs, examples
4. Test with Claude
5. Run tests: `make test`
6. Git commit + push

### Available Makefile Commands
```bash
make help      # Show all commands
make install   # Install dependencies
make dev       # Install with dev deps
make lint      # Check code quality
make format    # Format code
make test      # Run tests
make clean     # Remove build artifacts
make cli       # Run the CLI
```

## Using uv Directly

### Install dependencies
```bash
uv pip install -e .
uv pip install -e ".[dev]"  # with dev deps
```

### Run commands
```bash
uv run playbooks list
uv run pytest tests/
uv run ruff check src/
```

### Python shell
```bash
uv run python
# Then in Python:
from playbooks import PromptLibrary
library = PromptLibrary()
prompts = library.list_prompts()
```

## Project Structure

```
playbooks/
├── src/playbooks/       # Main package
│   ├── library.py       # PromptLibrary class
│   └── __init__.py
├── src/cli/
│   └── main.py          # CLI commands
├── prompts/             # YAML prompt templates
│   ├── deployment/
│   ├── cost_optimization/
│   ├── incident_response/
│   ├── compliance/
│   └── security/
├── tests/               # Test files
├── examples/            # Usage examples
├── Makefile             # Quick commands
├── pyproject.toml       # Dependencies
└── .python-version      # Python 3.11
```

## Troubleshooting

### `command not found: uv`
Install uv:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### `ImportError: No module named 'playbooks'`
Install in editable mode:
```bash
uv pip install -e .
```

### Tests fail
Make sure dev dependencies are installed:
```bash
make dev
```

## Tips

- Use `uv pip` instead of `pip` (much faster)
- Use `make` commands for common tasks
- Run `make test` before committing
- Run `make format` to auto-fix style issues
