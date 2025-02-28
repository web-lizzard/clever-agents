import yaml
from pathlib import Path

class PromptBuilder:
    def __init__(self, content: str):
        self.content = content
        self.context = None
        self.examples = None
    
    def with_context(self, context: str) -> 'PromptBuilder':
        self.context = f"<context>{context}</context>"
        return self
    
    def with_examples(self, path: Path) -> 'PromptBuilder':
        if not path.exists():
            raise FileNotFoundError(f"File {path} doet not exist")
        
        with open(path, 'r', encoding='utf-8') as file:
            examples_data = yaml.safe_load(file)
        
        formatted_examples = []
        for example in examples_data.get('examples', []):
            formatted_example = f"<example>\n  <input>{example.get('input', '')}</input>\n  <output>{example.get('output', '')}</output>\n</example>"
            formatted_examples.append(formatted_example)
        
        self.examples = "<examples>\n" + "\n".join(formatted_examples) + "\n</examples>"
        return self
    
    def build(self) -> str:
        """Zwraca finalny prompt ze wszystkimi dodanymi elementami."""
        result = self.content
        
        if self.context:
            result += f"\n\n{self.context}"
            
        if self.examples:
            result += f"\n\n{self.examples}"
            
        return result
