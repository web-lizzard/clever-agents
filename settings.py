from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class LanguageModelSettings(BaseModel):
    api_key: str

class Settings(BaseSettings):
    llm_settings: LanguageModelSettings

    model_config = SettingsConfigDict(
        env_nested_delimiter="__", env_file='.env'
    )


settings = Settings()