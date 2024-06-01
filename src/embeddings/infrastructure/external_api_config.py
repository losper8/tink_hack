from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ExternalApiConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='EXTERNAL_API_')

    OPENAI_TOKEN: str = Field("...")
    OPENAI_MODEL_NAME: str = Field("text-embedding-3-large")
    OPENAI_MODEL_ENCODER_NAME: str = Field("cl100k_base")
    OPENAI_MODEL_MAX_INPUT: int = Field(8192)


external_api_config = ExternalApiConfig()
