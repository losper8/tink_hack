from chromadb import EmbeddingFunction, Documents, Embeddings
from langchain_community.embeddings import GigaChatEmbeddings
from transformers import AutoModel
from sentence_transformers import SentenceTransformer

from embeddings.infrastructure.config import giga_chat_api_config


class GigaChatEmbeddingFunction(EmbeddingFunction[Documents]):
    def __init__(self, credentials: str, scope: str):
        self.embeddings = GigaChatEmbeddings(credentials=credentials, verify_ssl_certs=False, scope=scope)

    def __call__(self, input: Documents) -> Embeddings:
        return self.embeddings.embed_documents(texts=input)


# async?

gigachat_embedding_function = GigaChatEmbeddingFunction(credentials=giga_chat_api_config.TOKEN,
                                                        scope=giga_chat_api_config.SCOPE)


