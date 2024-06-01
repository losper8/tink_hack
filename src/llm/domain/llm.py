from langchain.chat_models.gigachat import GigaChat
from langchain_openai import OpenAI
from llm.infrastructure.config import giga_chat_api_config

giga_chat_llm = GigaChat(
    credentials=giga_chat_api_config.TOKEN,
    scope=giga_chat_api_config.SCOPE,
    verify_ssl_certs=False,
    timeout=120,
)
giga_chat_llm.temperature = 1e-10
giga_chat_llm.max_tokens = 1024

openai_llm = OpenAI(openai_api_key="AQVN1QYhY-29ScLDCbm8O0LnQ2b9kvEviIV-B7EF", openai_organization="ajel0ogm7rdt971c62dp")