import asyncio
import re
from typing import List, Optional, Tuple

from anyio import Path

from language_model.base import LLMCall
from language_model.openai import OpenAILLMCall

from .context_generator import ContextGenerator, LLMContextGenerator
from .schemas import Document, DocumentMetadata
from .tokenizer import TiktokenTokenizer, Tokenizer


class TextSplitter:
    def __init__(self, tokenizer: Optional[Tokenizer] = None, context_generator: ContextGenerator | None = None):
        """
        Inicjalizuje TextSplitter z podanym tokenizerem.
        
        Args:
            tokenizer: Implementacja TokenizerProtocol. Jeśli nie podano, używa domyślnego TiktokenTokenizer.
        """
        self.tokenizer = tokenizer if tokenizer is not None else TiktokenTokenizer()
        self.context_generator = context_generator

    async def split(self, text: str, limit: int) -> List[Document]:
        print(f"Starting split process with limit: {limit} tokens")
        chunks = []
        position = 0
        total_length = len(text)
        current_headers = {}

        while position < total_length:
            print(f"Processing chunk starting at position: {position}")
            chunk_text, chunk_end = self.get_chunk(text, position, limit)
            tokens = self.tokenizer.count_tokens(chunk_text)
            print(f"Chunk tokens: {tokens}")

            headers_in_chunk = self.extract_headers(chunk_text)
            self.update_current_headers(current_headers, headers_in_chunk)

            content, urls, images = self.extract_urls_and_images(chunk_text)
            context = None
            if self.context_generator:
                context =  await self.context_generator.generate_context(content, text)

            chunks.append(Document(
                text=content,
                metadata=DocumentMetadata(
                    tokens=tokens,
                    headers=current_headers,
                    urls=urls,
                    images=images,
                    context=context
                )
            ))

            print(f"Chunk processed. New position: {chunk_end}")
            position = chunk_end

        print(f"Split process completed. Total chunks: {len(chunks)}")
        return chunks

    def get_chunk(self, text: str, start: int, limit: int) -> Tuple[str, int]:
        print(f"Getting chunk starting at {start} with limit {limit}")
        
        empty_text_tokens = self.tokenizer.count_tokens('')
        formatted_empty_text_tokens = self.tokenizer.count_tokens(self.tokenizer.format_for_tokenization(''))
        overhead = formatted_empty_text_tokens - empty_text_tokens
        
        if start >= len(text):
            return "", start
            
        remaining_text = text[start:]
        remaining_tokens = self.tokenizer.count_tokens(remaining_text)
        
        if remaining_tokens == 0:
            return "", start
            
        end = min(start + int(len(remaining_text) * limit / remaining_tokens), len(text))
        
        chunk_text = text[start:end]
        tokens = self.tokenizer.count_tokens(chunk_text)
        
        while tokens + overhead > limit and end > start:
            print(f"Chunk exceeds limit with {tokens + overhead} tokens. Adjusting end position...")
            end = self.find_new_chunk_end(text, start, end)
            chunk_text = text[start:end]
            tokens = self.tokenizer.count_tokens(chunk_text)

        end = self.adjust_chunk_end(text, start, end, tokens + overhead, limit)

        chunk_text = text[start:end]
        tokens = self.tokenizer.count_tokens(chunk_text)
        print(f"Final chunk end: {end}")
        return chunk_text, end

    def adjust_chunk_end(self, text: str, start: int, end: int, current_tokens: int, limit: int) -> int:
        min_chunk_tokens = limit * 0.8

        next_newline = text.find('\n', end)
        prev_newline = text.rfind('\n', start, end)

        if next_newline != -1 and next_newline < len(text):
            extended_end = next_newline + 1
            chunk_text = text[start:extended_end]
            tokens = self.tokenizer.count_tokens(chunk_text)
            if tokens <= limit and tokens >= min_chunk_tokens:
                print(f"Extending chunk to next newline at position {extended_end}")
                return extended_end

        if prev_newline > start:
            reduced_end = prev_newline + 1
            chunk_text = text[start:reduced_end]
            tokens = self.tokenizer.count_tokens(chunk_text)
            if tokens <= limit and tokens >= min_chunk_tokens:
                print(f"Reducing chunk to previous newline at position {reduced_end}")
                return reduced_end

        return end

    def find_new_chunk_end(self, text: str, start: int, end: int) -> int:
        new_end = end - int((end - start) / 10)
        if new_end <= start:
            new_end = start + 1
        return new_end

    def extract_headers(self, text: str) -> dict:
        headers = dict()
        header_regex = re.compile(r'(^|\n)(#{1,6})\s+(.*)')
        for match in header_regex.finditer(text):
            level = len(match.group(2))
            content = match.group(3).strip()
            key = f'h{level}'
            headers.setdefault(key, []).append(content)
        return headers

    def update_current_headers(self, current: dict, extracted: dict):
        for level in range(1, 7):
            key = f'h{level}'
            if key in extracted:
                current[key] = extracted[key]
                self.clear_lower_headers(current, level)

    def clear_lower_headers(self, headers: dict, level: int):
        for l in range(level + 1, 7):
            headers.pop(f'h{l}', None)

    def extract_urls_and_images(self, text: str) -> Tuple[str, List[str], List[str]]:
        urls = []
        images = []
        url_index = 0
        image_index = 0

        def replace_image(match):
            nonlocal image_index
            alt_text = match.group(1)
            url = match.group(2)
            images.append(url)
            result = f"![{alt_text}]({{{{$img{image_index}}}}})"
            image_index += 1
            return result

        def replace_url(match):
            nonlocal url_index
            link_text = match.group(1)
            url = match.group(2)
            urls.append(url)
            result = f"[{link_text}]({{{{$url{url_index}}}}})"
            url_index += 1
            return result

        content = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', replace_image, text)
        content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', replace_url, content)

        return content, urls, images



