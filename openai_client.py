from openai import AsyncOpenAI
from langfuse.openai import AsyncOpenAI as LangfuseOpenAI
from langfuse.openai import openai

from settings import settings

def get_client(with_observability: bool = False) -> AsyncOpenAI:
 
    if with_observability:
        openai.langfuse_public_key = settings.observability_settings.public_key
        openai.langfuse_secret_key = settings.observability_settings.secret_key
        openai.langfuse_host = settings.observability_settings.host
        return LangfuseOpenAI(api_key=settings.llm_settings.api_key)

    return AsyncOpenAI(
        api_key=settings.llm_settings.api_key
    )