from abc import ABC, abstractmethod
from pathlib import Path

from openai import BaseModel

from language_model import LLMCall
from language_model.prompt.builder import PromptBuilder
from language_model.schemas import ChatConversation


class ContextGenerator(ABC):

    @abstractmethod
    async def generate_context(self, chunk: str, original_text: str) -> str:
        pass



class Context(BaseModel):
    context: str


class LLMContextGenerator(ContextGenerator):

    def __init__(self, call: LLMCall) -> None:
        self._call = call
        

    
    async def generate_context(self, chunk: str, original_text: str) -> str:
        prompt_builder = self._get_prompt(chunk, original_text)
        conversation = self._get_chat_conversation(prompt_builder)
        
        response = await self._call.generate_structured_output(messages=conversation, response_model=Context, temperature=0.0)

        return response.context
    
    def _get_prompt(self, chunk: str, original_text: str) -> PromptBuilder:
        main_body = (
            "Analyze the document chunk in context of full document\n"
            f"<full_document>\n{original_text}\n</full_document>\n\n"
            "Generate contextual metadata for this chunk:"
        )
        
        return (
            PromptBuilder(main_body)
            .with_title("Contextual Retrieval Prompt")
            .with_rules([
                "Focus on hierarchical relationships within document",
                "Extract temporal/causal connections",
                "Preserve XML structure in response",
                "Never invent information not present in document"
            ])
            .with_context({
                "chunk": chunk
            })
            .with_examples(Path("prompts/examples/context_retrieval_examples.yaml"))
            .with_confirmation("Remember: Only return the contextual information, nothing else")
        )
    
    def _get_chat_conversation(self, builder: PromptBuilder) -> ChatConversation:
        conversation = ChatConversation()

        conversation.add_system_message(builder.build())
        
        return conversation
