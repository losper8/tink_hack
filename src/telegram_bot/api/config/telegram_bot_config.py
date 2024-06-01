from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class TelegramBotConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='TELEGRAM_BOT_')
    TOKEN: str = Field(env="TOKEN")


telegram_bot_config = TelegramBotConfig()
