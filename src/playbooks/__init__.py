"""
Playbooks - Battle-tested prompts for infrastructure agents.

Like Ansible playbooks, but for AI.
"""

__version__ = "0.1.0"
__author__ = "Brian Hopkins"

from .library import Prompt, PromptLibrary

__all__ = ["PromptLibrary", "Prompt"]
