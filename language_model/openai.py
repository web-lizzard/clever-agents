from typing import AsyncGenerator, Type

from openai import AsyncOpenAI

from .base import LLMCall, ResponseT
from .schemas import ChatConversation


class OpenAILLMCall(LLMCall):
    """
    Implementation of language model for OpenAI API with structured output support.
    """

    def __init__(
        self,
        client: AsyncOpenAI,
        model_name: str = 'gpt-4o-mini'
    ):
        """
        Initialize the OpenAI structured output model.

        Args:
            model_name: Name of the OpenAI model to use (e.g., "gpt-4o")
            response_model: Pydantic model class that defines the expected response structure
            client: AsyncOpenAI client instance
            messages:
        """
        self._client = client
        self._model_name = model_name

    async def generate_structured_output(
        self, messages: ChatConversation, response_model: Type[ResponseT], temperature: float = 0.7, model_name: str = 'gpt-4o-mini'
    ) -> ResponseT:
        """
        Generate structured output using OpenAI's beta.chat.completions.parse method.

        Args:
            message: User message or prompt
            temperature: Randomness parameter (0.0-2.0)

        Returns:
            Structured response conforming to the specified response model
        """

        completion = await self._client.beta.chat.completions.parse(
            messages=messages.to_openai_format(),
            model=model_name,
            response_format=response_model,
            temperature=temperature
        )

        parsed_response = completion.choices[0].message.parsed

        if parsed_response is None:
            raise ValueError("Failed to parse response into the specified model")

        return parsed_response

    async def generate_stream(
        self, messages: ChatConversation, temperature: float = 0.7
    ) -> AsyncGenerator[str, None]:
        """
        Stream the response from OpenAI API.
        
        Args:
            messages: ChatML document containing conversation history
            temperature: Randomness parameter (0.0-1.0)
            
        Yields:
            Text chunks from the streaming response
        """
        stream = await self._client.chat.completions.create(
            model=self._model_name,
            messages=messages.to_openai_format(),
            temperature=temperature,
            stream=True
        )
        
        async for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content        
