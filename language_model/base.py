from abc import ABC, abstractmethod
from typing import AsyncGenerator, Protocol, Type, TypeVar

from pydantic import BaseModel

from .schemas import ChatConversation

ResponseT = TypeVar("ResponseT", bound=BaseModel)


class LLMCall(ABC):
    """
    Abstract base class for language model interactions.
    Parameterized with response type (ResponseT), which must inherit from BaseModel from pydantic.
    """
    @abstractmethod
    async def generate_structured_output(
        self, messages: ChatConversation, response_model: Type[ResponseT], temperature: float, model_name: str
    ) -> ResponseT:
        """
        Abstract method for asynchronously calling a language model
        and obtaining a structured response.

        Args:
            messages: Message to be processed by the model in ChatMLDocument format
            temperature: Randomness parameter (higher value = more random responses)

        Returns:
            Structured model response conforming to ResponseT type
        """
        raise NotImplementedError


    @abstractmethod
    async def generate_stream(self, messages: ChatConversation, temperature: float, model_name: str) -> AsyncGenerator[str, None]:
        raise NotImplementedError
