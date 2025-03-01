from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class LanguageModelSettings(BaseModel):
    api_key: str

class LLMObservabilityToolSettings(BaseModel):
    public_key: str
    secret_key: str
    host: str

class Settings(BaseSettings):
    llm_settings: LanguageModelSettings
    observability_settings: LLMObservabilityToolSettings

    model_config = SettingsConfigDict(
        env_nested_delimiter="__", env_file='.env', extra='allow'
    )


settings = Settings()