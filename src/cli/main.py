"""CLI for playbooks prompt management."""

import click
from rich.console import Console
from rich.table import Table
from pathlib import Path
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from playbooks.library import PromptLibrary

console = Console()


@click.group()
def main():
    """Playbooks - Battle-tested prompts for infrastructure agents.
    
    Like Ansible playbooks, but for AI.
    
    Commands:
      list     List all available prompts
      show     Show details of a specific prompt
      search   Search prompts by keyword
      test     Test a prompt
    """
    pass


@main.command()
@click.option("--category", "-c", help="Filter by category")
def list(category):
    """List all available prompts."""
    library = PromptLibrary()
    
    if category:
        prompts = library.list_prompts(category)
    else:
        prompts = library.list_prompts()
    
    if not prompts:
        console.print("[yellow]No prompts found[/yellow]")
        return
    
    table = Table(title="Available Prompts")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Category", style="magenta")
    table.add_column("Version", style="blue")
    table.add_column("Quality", style="yellow")
    
    for prompt in sorted(prompts, key=lambda p: p.category):
        quality = f"{prompt.get_quality_score():.2f}"
        table.add_row(
            prompt.id,
            prompt.name,
            prompt.category,
            prompt.version,
            quality,
        )
    
    console.print(table)
    console.print(f"\n[bold]Total: {len(prompts)} prompts[/bold]")


@main.command()
@click.argument("prompt_id")
def show(prompt_id):
    """Show details of a specific prompt."""
    library = PromptLibrary()
    
    prompt = None
    for p in library.prompts.values():
        if p.id == prompt_id or prompt_id in p.id:
            prompt = p
            break
    
    if not prompt:
        console.print(f"[red]Prompt '{prompt_id}' not found[/red]")
        return
    
    console.print(f"\n[bold cyan]{prompt.name}[/bold cyan]")
    console.print(f"ID: {prompt.id}")
    console.print(f"Category: {prompt.category}")
    console.print(f"Version: {prompt.version}")
    console.print(f"Quality Score: {prompt.get_quality_score()}")
    console.print(f"Production Tested: {prompt.is_production_tested()}")
    console.print(f"Test Count: {prompt.get_test_count()}\n")
    
    if prompt.inputs:
        console.print("[bold]Inputs:[/bold]")
        for inp in prompt.inputs:
            console.print(f"  - {inp.get('name')}: {inp.get('description')}")
    
    if prompt.outputs:
        console.print("\n[bold]Outputs:[/bold]")
        for out in prompt.outputs:
            console.print(f"  - {out.get('name')}: {out.get('description')}")
    
    console.print(f"\n[bold]Prompt:[/bold]\n{prompt.prompt_text}\n")


@main.command()
@click.argument("keyword")
def search(keyword):
    """Search prompts by keyword."""
    library = PromptLibrary()
    results = library.search(keyword)
    
    if not results:
        console.print(f"[yellow]No prompts found matching '{keyword}'[/yellow]")
        return
    
    table = Table(title=f"Search Results: '{keyword}'")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Category", style="magenta")
    
    for prompt in results:
        table.add_row(prompt.id, prompt.name, prompt.category)
    
    console.print(table)


@main.command()
def version():
    """Show version."""
    from playbooks import __version__
    console.print(f"[bold]Playbooks[/bold] v{__version__}")


if __name__ == "__main__":
    main()
