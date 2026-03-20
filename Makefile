.PHONY: help install dev lint lint-fix format test clean

help:
	@echo "Playbooks - Battle-tested prompts for infrastructure agents"
	@echo ""
	@echo "Available commands:"
	@echo "  make install    Install dependencies with uv"
	@echo "  make dev        Install with dev dependencies"
	@echo "  make lint       Run linting checks (ruff, mypy)"
	@echo "  make lint-fix   Auto-fix lint and formatting issues"
	@echo "  make format     Format code with ruff"
	@echo "  make test       Run tests with pytest"
	@echo "  make clean      Remove build artifacts"
	@echo "  make cli        Run CLI (playbooks)"

install:
	uv pip install -e .

dev:
	uv pip install -e ".[dev]"

lint:
	@echo "Running ruff..."
	uv run ruff check src/ tests/
	@echo "Running mypy..."
	uv run mypy src/playbooks

lint-fix:
	@echo "Fixing lint issues..."
	uv run ruff check --fix --unsafe-fixes src/ tests/
	uv run ruff format src/ tests/
	@echo "Running mypy..."
	uv run mypy src/playbooks

format:
	uv run ruff format src/ tests/
	uv run ruff check --fix src/ tests/

test:
	uv run pytest tests/ -v --cov=src/playbooks

cli:
	uv run playbooks

clean:
	rm -rf build/ dist/ *.egg-info .pytest_cache .mypy_cache .ruff_cache htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

.DEFAULT_GOAL := help
