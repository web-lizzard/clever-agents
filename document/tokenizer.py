from typing import Protocol

import tiktoken


class Tokenizer(Protocol):  
    """Protokół definiujący interfejs dla tokenizatorów."""
    def count_tokens(self, text: str) -> int:
        """Zlicza tokeny w podanym tekście."""
        ...

    def format_for_tokenization(self, text: str) -> str:
        """Formatuje tekst przed tokenizacją."""
        ...

class TiktokenTokenizer:
    """Implementacja tokenizatora wykorzystująca bibliotekę tiktoken."""
    
    def __init__(self, model_name: str = "gpt-4o"):
        self.model_name = model_name
        self.tokenizer = tiktoken.encoding_for_model(model_name)
        self.special_tokens = {
            '<|im_start|>': 100264,
            '<|im_end|>': 100265,
            '<|im_sep|>': 100266,
        }
        
    def count_tokens(self, text: str) -> int:
        """Zlicza tokeny w podanym tekście."""
        formatted_text = self.format_for_tokenization(text)
        return len(self.tokenizer.encode(formatted_text))
    
    def format_for_tokenization(self, text: str) -> str:
        """Formatuje tekst przed tokenizacją."""
        return f"<|im_start|>user\n{text}<|im_end|>\n<|im_start|>assistant<|im_end|>"