"""Tests for CLI module."""

import pytest
from click.testing import CliRunner
from playbooks.cli.main import main


class TestCLI:
    """Test CLI commands."""
    
    @pytest.fixture
    def runner(self):
        """Create a CLI runner."""
        return CliRunner()
    
    def test_cli_help(self, runner):
        """Test help command."""
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "Playbooks" in result.output
    
    def test_cli_version(self, runner):
        """Test version command."""
        result = runner.invoke(main, ["version"])
        assert result.exit_code == 0
        assert "Playbooks" in result.output
        assert "0.1.0" in result.output
    
    def test_cli_list(self, runner):
        """Test list command."""
        result = runner.invoke(main, ["list"])
        assert result.exit_code == 0
        assert "Available Prompts" in result.output
        assert "deployment" in result.output.lower()
    
    def test_cli_list_by_category(self, runner):
        """Test list command with category filter."""
        result = runner.invoke(main, ["list", "--category", "deployment"])
        assert result.exit_code == 0
        assert "deployment" in result.output.lower()
    
    def test_cli_list_nonexistent_category(self, runner):
        """Test list with non-existent category."""
        result = runner.invoke(main, ["list", "--category", "nonexistent"])
        assert result.exit_code == 0
        assert "No prompts found" in result.output
    
    def test_cli_show(self, runner):
        """Test show command."""
        result = runner.invoke(main, ["show", "deployment-canary-001"])
        assert result.exit_code == 0
        assert "Canary Rollout Strategy" in result.output
        assert "Inputs:" in result.output
        assert "Outputs:" in result.output
    
    def test_cli_show_nonexistent(self, runner):
        """Test show with non-existent prompt."""
        result = runner.invoke(main, ["show", "nonexistent-999"])
        assert result.exit_code == 0
        assert "not found" in result.output
    
    def test_cli_search(self, runner):
        """Test search command."""
        result = runner.invoke(main, ["search", "canary"])
        assert result.exit_code == 0
        assert "Search Results" in result.output
        assert "canary" in result.output.lower()
    
    def test_cli_search_no_results(self, runner):
        """Test search with no results."""
        result = runner.invoke(main, ["search", "nonexistent_xyz"])
        assert result.exit_code == 0
        assert "No prompts found" in result.output
