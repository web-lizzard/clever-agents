from abc import ABC
from typing import Callable, Self

import gradio as gr


class ChatBotBuilder(ABC):
    
    def with_markdown_ouput(self, label: str) -> Self:
        raise NotImplementedError


    def with_textbox_input(self, label: str) -> Self:
        raise NotImplementedError


    def build(self, handler: Callable)-> None:
        raise NotImplementedError



class GradioChatbotBuilder(ChatBotBuilder):
    def __init__(self) -> None:
        self._outputs = []
        self._inputs = []


    def with_markdown_ouput(self, label: str) -> Self:
        self._outputs.append(gr.Markdown(label=label))

        return self

    def with_textbox_input(self, label: str) -> Self:
        self._inputs.append(gr.Textbox(label=label))

        return self

    def build(self, handler: Callable)-> None:
        gr.Interface(fn=handler, inputs=self._inputs, outputs=self._outputs, flagging_mode='never', concurrency_limit=5).launch()   
