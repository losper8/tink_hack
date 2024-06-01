from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ChromaDBConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='CHROMA_DB_')

    HOST: str = Field("chromadb")
    PORT: int = Field(8000)


chroma_db_config = ChromaDBConfig()
