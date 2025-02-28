from language_model import OpenAILLMCall
from language_model.schemas import ChatMLDocument, ChatMessage, RoleType
from language_model.prompt import PromptBuilder

from openai import AsyncOpenAI

from pydantic import BaseModel

from settings import settings

class Hello(BaseModel):
    msg: str


async def main():
    print("Hello from clever-agents!")

    client = AsyncOpenAI(
        api_key=settings.llm_settings.api_key
    )

    llm_call = OpenAILLMCall(response_model=Hello, client=client)

    document = ChatMLDocument(
        messages=[
            ChatMessage(
                role=RoleType.SYSTEM, content=PromptBuilder("You are a helpful assistant, your name is Zod, and my name is Adrian").build()
            ),
            ChatMessage(role=RoleType.USER, content="Hello what's your name"),
        ]
    )

    response = await llm_call.generate_structured_output(messages=document)

    print(response.msg)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
