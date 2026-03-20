"""Core PromptLibrary for loading and managing prompts."""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from pathlib import Path
import yaml


@dataclass
class Prompt:
    """Single prompt from the library."""
    
    id: str
    name: str
    category: str
    version: str
    prompt_text: str
    metadata: Dict[str, Any]
    inputs: List[Dict[str, Any]]
    outputs: List[Dict[str, Any]]
    
    def customize(self, **kwargs) -> str:
        """Customize prompt with user parameters."""
        return self.prompt_text.format(**kwargs)
    
    def get_quality_score(self) -> float:
        """Return prompt quality score (0-1)."""
        return self.metadata.get("quality_score", 0.0)
    
    def get_test_count(self) -> int:
        """Return number of production tests."""
        return self.metadata.get("test_count", 0)
    
    def is_production_tested(self) -> bool:
        """Check if prompt has been tested in production."""
        return self.metadata.get("production_tested", False)


class PromptLibrary:
    """Load and manage prompts from YAML files."""
    
    def __init__(self, prompts_dir: Optional[Path] = None):
        """Initialize library with prompts directory.
        
        Args:
            prompts_dir: Path to prompts directory. Defaults to ./prompts
        """
        if prompts_dir is None:
            prompts_dir = Path(__file__).parent.parent.parent / "prompts"
        
        self.prompts_dir = prompts_dir
        self.prompts: Dict[str, Prompt] = {}
        self._load_all()
    
    def _load_all(self) -> None:
        """Load all YAML prompts from directory."""
        if not self.prompts_dir.exists():
            return
        
        for yaml_file in self.prompts_dir.rglob("*.yaml"):
            try:
                with open(yaml_file, encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                
                if not data or "metadata" not in data:
                    continue
                
                prompt = Prompt(
                    id=data["metadata"].get("id", ""),
                    name=data["metadata"].get("name", ""),
                    category=data["metadata"].get("category", ""),
                    version=data["metadata"].get("version", ""),
                    prompt_text=data.get("prompt_text", ""),
                    metadata=data["metadata"],
                    inputs=data.get("inputs", []),
                    outputs=data.get("outputs", []),
                )
                self.prompts[prompt.id] = prompt
            except Exception as e:
                print(f"Warning: Failed to load {yaml_file}: {e}")
    
    def get_prompt(self, category: str, task_name: Optional[str] = None) -> Optional[Prompt]:
        """Get prompt by category and optional task name.
        
        Args:
            category: Prompt category (e.g., "deployment", "cost_optimization")
            task_name: Optional task name to filter by
        
        Returns:
            Prompt if found, None otherwise
        """
        for prompt in self.prompts.values():
            if prompt.category == category:
                if task_name is None:
                    return prompt
                if task_name.lower() in prompt.id.lower():
                    return prompt
        return None
    
    def list_prompts(self, category: Optional[str] = None) -> List[Prompt]:
        """List available prompts.
        
        Args:
            category: Optional category to filter by
        
        Returns:
            List of prompts
        """
        if category:
            return [p for p in self.prompts.values() if p.category == category]
        return list(self.prompts.values())
    
    def list_categories(self) -> List[str]:
        """List all available categories."""
        return sorted(set(p.category for p in self.prompts.values()))
    
    def search(self, keyword: str) -> List[Prompt]:
        """Search prompts by keyword.
        
        Args:
            keyword: Keyword to search for
        
        Returns:
            List of matching prompts
        """
        keyword = keyword.lower()
        return [
            p for p in self.prompts.values()
            if keyword in p.name.lower() or keyword in p.id.lower()
        ]
