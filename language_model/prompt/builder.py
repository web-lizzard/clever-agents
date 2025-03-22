import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Self, Union

import yaml


@dataclass
class Prompt:
    """
    A prompt abstraction that behaves like a string and can be serialized to JSON.
    """
    content: str
    
    def __str__(self) -> str:
        """Make the Prompt behave like a string."""
        return self.content
    
    def __repr__(self) -> str:
        """String representation of the prompt."""
        if len(self.content) > 50:
            return f"Prompt({repr(self.content)[:50]}...)"
        return f"Prompt({repr(self.content)})"
    
    def write_json(self, filepath: Union[str, Path]) -> None:
        """
        Write the prompt to a JSON file in a format suitable for chat-based LLMs.
        
        Args:
            filepath: Path to the output JSON file.
        """
        data = [
            {
                "role": "system",
                "content": self.content
            }
        ]
        
        with open(Path(filepath), 'w') as f:
            json.dump(data, f, indent=2)


class PromptBuilder:
    def __init__(self, body: str) -> None:
        """
        Initialize the PromptBuilder with the main body of a prompt.
        
        Args:
            body: The main body of the prompt (concise explanation).
        """
        self._body: str = body
        self._title: Optional[str] = None
        self._examples: List[dict] = []
        self._rules: List[str] = []
        self._context: Optional[str] = None
        self._confirmation: Optional[str] = None
    
    def with_title(self, title: str) -> Self:
        """
        Add a title to the prompt.
        
        Args:
            title: The title to add.
            
        Returns:
            The builder instance for method chaining.
        """
        self._title = title
        return self
    
    def with_examples(self, yaml_path: Union[str, Path]) -> Self:
        """
        Add examples to the prompt, parsed from a YAML file.
        
        Args:
            yaml_path: Path to the YAML file containing examples.
                       Format should be example_n: {request: "...", response: "..."}
            
        Returns:
            The builder instance for method chaining.
        """
        path = Path(yaml_path)
        with open(path, 'r') as file:
            examples_data = yaml.safe_load(file)
            
        for key, value in examples_data.items():
            if key.startswith('example_') and isinstance(value, dict):
                if 'request' in value and 'response' in value:
                    self._examples.append({
                        'request': value['request'],
                        'response': value['response']
                    })
        
        return self
    
    def with_rules(self, rules: List[str]) -> Self:
        """
        Add rules to the prompt.
        
        Args:
            rules: List of rules to add.
            
        Returns:
            The builder instance for method chaining.
        """
        self._rules = rules
        return self
    
    def with_context(self, context: str) -> Self:
        """
        Add additional context to the prompt.
        
        Args:
            context: The context information to add.
            
        Returns:
            The builder instance for method chaining.
        """
        self._context = context
        return self
    
    def with_confirmation(self, confirmation: str) -> Self:
        """
        Add a final confirmation to the prompt.
        
        Args:
            confirmation: The confirmation message.
            
        Returns:
            The builder instance for method chaining.
        """
        self._confirmation = confirmation
        return self
    
    def build(self) -> Prompt:
        """
        Build and return the complete prompt according to the specified format.
        
        Returns:
            A Prompt object that behaves like a string and can be serialized to JSON.
        """
        prompt_parts: List[str] = []
        
        if self._title:
            prompt_parts.append(f"{self._title}")
            prompt_parts.append("")  # Empty line
        
        prompt_parts.append(f"{self._body}")
        prompt_parts.append("")  # Empty line
        
        if self._rules:
            prompt_parts.append("<rules>")
            prompt_parts.append("")
            for rule in self._rules:
                prompt_parts.append(f"- {rule}")
            prompt_parts.append("")
            prompt_parts.append("</prompt_rules>")
            prompt_parts.append("")
        
        if self._context:
            prompt_parts.append("<context>")
            prompt_parts.append(self._context)
            prompt_parts.append("</context>")
            prompt_parts.append("")
        
        if self._examples:
            prompt_parts.append("<examples>")
            for i, example in enumerate(self._examples):
                if i > 0:  # Add an empty line between examples
                    prompt_parts.append("")
                prompt_parts.append(f"USER: {example['request']}")
                prompt_parts.append(f"AI: {example['response']}")
            prompt_parts.append("")
            prompt_parts.append("</examples>")
            prompt_parts.append("")
        
        if self._confirmation:
            prompt_parts.append(f"{self._confirmation}")
        
        return Prompt("\n".join(prompt_parts))
