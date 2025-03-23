import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Self, Union

import yaml


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
    
    def with_context(self, context: dict[str, str]) -> Self:
        """
        Add additional context to the prompt in XML-like format.
        
        Args:
            context: Dictionary where keys are section names and values are the content.
                    Each section will be formatted as <key>value</key>.
                
        Returns:
            The builder instance for method chaining.
        """
        # Format the context as XML-like tags
        formatted_sections = []
        for key, value in context.items():
            formatted_sections.append(f"<{key}>{value}</{key}>")
        
        # Join all formatted sections with newlines
        self._context = "\n".join(formatted_sections)
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
    
    def build(self) -> str:
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
            prompt_parts.append(self._context)
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
        
        return "\n".join(prompt_parts)
