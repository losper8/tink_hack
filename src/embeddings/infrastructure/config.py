import os
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class GigaChatApiConfig(BaseSettings):
    model_config = SettingsConfigDict( env_prefix='GIGA_CHAT_API_')
    TOKEN: str = Field(...)
    SCOPE: Optional[str] = Field(None)


giga_chat_api_config = GigaChatApiConfig()
