from typing import Type
from openai import AsyncOpenAI
from .base import LLMCall, ResponseT

from .schemas import ChatMLDocument


class OpenAILLMCall(LLMCall[ResponseT]):
    """
    Implementation of language model for OpenAI API with structured output support.
    """

    def __init__(
        self,
        response_model: Type[ResponseT],
        client: AsyncOpenAI,
        model_name: str = "gpt-4o-mini",
    ):
        """
        Initialize the OpenAI structured output model.

        Args:
            model_name: Name of the OpenAI model to use (e.g., "gpt-4o")
            response_model: Pydantic model class that defines the expected response structure
            client: AsyncOpenAI client instance
            messages:
        """
        self._model_name = model_name
        self._response_model = response_model
        self._client = client

    async def generate_structured_output(
        self, messages: ChatMLDocument, temperature: float = 0.7
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
            messages=messages.to_list(),
            model=self._model_name,
            response_format=self._response_model,
            temperature=temperature
        )

        parsed_response = completion.choices[0].message.parsed

        if parsed_response is None:
            raise ValueError("Failed to parse response into the specified model")

        return parsed_response
