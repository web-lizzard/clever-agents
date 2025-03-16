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
        self.body: str = body
        self.title: Optional[str] = None
        self.examples: List[dict] = []
        self.rules: List[str] = []
        self.context: Optional[str] = None
        self.confirmation: Optional[str] = None
    
    def with_title(self, title: str) -> Self:
        """
        Add a title to the prompt.
        
        Args:
            title: The title to add.
            
        Returns:
            The builder instance for method chaining.
        """
        self.title = title
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
                    self.examples.append({
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
        self.rules = rules
        return self
    
    def with_context(self, context: str) -> Self:
        """
        Add additional context to the prompt.
        
        Args:
            context: The context information to add.
            
        Returns:
            The builder instance for method chaining.
        """
        self.context = context
        return self
    
    def with_confirmation(self, confirmation: str) -> Self:
        """
        Add a final confirmation to the prompt.
        
        Args:
            confirmation: The confirmation message.
            
        Returns:
            The builder instance for method chaining.
        """
        self.confirmation = confirmation
        return self
    
    def build(self) -> str:
        """
        Build and return the complete prompt according to the specified format.
        
        Returns:
            The complete prompt as a string.
        """
        prompt_parts: List[str] = []
        
        if self.title:
            prompt_parts.append(f"{self.title}")
            prompt_parts.append("")
        
        prompt_parts.append(f"{self.body}")
        prompt_parts.append("")
        
        if self.rules:
            prompt_parts.append("<rules>")
            prompt_parts.append("")
            for rule in self.rules:
                prompt_parts.append(f"- {rule}")
            prompt_parts.append("")
            prompt_parts.append("</rules>")
            prompt_parts.append("")
        
        if self.context:
            prompt_parts.append("<context>")
            prompt_parts.append(self.context)
            prompt_parts.append("</context>")
            prompt_parts.append("")
        
        if self.examples:
            prompt_parts.append("<examples>")
            for i, example in enumerate(self.examples):
                if i > 0:
                    prompt_parts.append("")
                prompt_parts.append(f"USER: {example['request']}")
                prompt_parts.append(f"AI: {example['response']}")
            prompt_parts.append("")
            prompt_parts.append("</examples>")
            prompt_parts.append("")
        
        if self.confirmation:
            prompt_parts.append(f"{self.confirmation}")
        
        return "\n".join(prompt_parts)
