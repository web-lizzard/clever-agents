from pydantic import BaseModel

from language_model import OpenAILLMCall
from language_model.prompt import PromptBuilder
from language_model.schemas import ChatMessage, ChatMLDocument, RoleType
from openai_client import get_client


class Hello(BaseModel):
    msg: str


async def main():
    client = get_client(with_observability=True)
    llm_call = OpenAILLMCall(response_model=Hello, client=client)
    document = ChatMLDocument(
        messages=[
            ChatMessage(
                role=RoleType.SYSTEM, content=PromptBuilder("You are a helpful assistant, your name is Zod. Remember that my name is Adrian.").build()
            ),
            ChatMessage(role=RoleType.USER, content="Hello what's my name"),
        ]
    )

    response = await llm_call.generate_structured_output(messages=document)

    print(response.msg)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
