from language_model.prompt import Prompt, PromptBuilder


def get_prompt() -> Prompt:

    return PromptBuilder("You are a helpful assistant").build()


if __name__ == '__main__':
    prompt = get_prompt()
    prompt.write_json('example.json')