import asyncio
from pathlib import Path

from document.context_generator import LLMContextGenerator
from document.splitter import TextSplitter
from language_model import OpenAILLMCall
from openai_client import get_client


async def main():
    llm_call = OpenAILLMCall(
        client=get_client(with_observability=True)
    )
    splitter = TextSplitter(context_generator=LLMContextGenerator(llm_call))
    article = Path() / 'example.md'

    docs = await splitter.split(article.read_text(), limit=300)
    for doc in docs:
        print(doc)
        print("context")
        print(doc.metadata.context)


if __name__ == "__main__":
    asyncio.run(main())
        