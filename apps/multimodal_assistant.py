from chatbot import ChatBotBuilder, GradioChatbotBuilder
from language_model import LLMCall, OpenAILLMCall
from language_model.prompt import PromptBuilder
from language_model.schemas import ChatConversation, ChatMessage


def get_chatbot_builder() -> ChatBotBuilder:

    return GradioChatbotBuilder().with_textbox_input('Your Input: ').with_markdown_ouput('Output')

def main():
    builder = get_chatbot_builder()


    builder.build(
        lambda: None
    )





if __name__ == '__main__':
    main()