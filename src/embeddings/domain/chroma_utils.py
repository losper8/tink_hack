from typing import List

import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings
from langchain_community.embeddings.gigachat import GigaChatEmbeddings
from tqdm import tqdm
from fastapi import Query

from embeddings.infrastructure.embedding_functions import GigaChatEmbeddingFunction
from embeddings.infrastructure.external_api_config import external_api_config
from embeddings.infrastructure.chroma_db_config import chroma_db_config
from embeddings.infrastructure.config import giga_chat_api_config

from embeddings.api.schema import SaveDataRequest, SearchRequest
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

openai_embedding_function = OpenAIEmbeddingFunction(api_key=external_api_config.OPENAI_TOKEN,
                                                    model_name=external_api_config.OPENAI_MODEL_NAME)

print("--------------->", external_api_config.OPENAI_TOKEN)

gigachat_embedding_function = GigaChatEmbeddingFunction(credentials=giga_chat_api_config.TOKEN,
                                                        scope=giga_chat_api_config.SCOPE)


chroma_client = chromadb.HttpClient(host=chroma_db_config.HOST, port=chroma_db_config.PORT)

openai_collection = chroma_client.get_or_create_collection(name='openai_collection',
                                                           embedding_function=openai_embedding_function)

gigachat_collection = chroma_client.get_or_create_collection(name='gigachat_collection',
                                                             embedding_function=gigachat_embedding_function)


async def add_vectors_to_db(request: SaveDataRequest):
    if request.encoding_model == 'openai':
        collection = openai_collection
    elif request.encoding_model == 'gigachat':
        collection = gigachat_collection
    else:
        return 'not valid encoding_model'

    try:
        documents = request.documents
        metadatas = request.metadatas
        batch_size = 500  # размер пакета для добавления

        start = collection.count()
        ids = [str(i) for i in range(start, start + len(documents))]

        for i in range(0, len(documents), batch_size):
            batch_ids = ids[i:i + batch_size]
            batch_docs = documents[i:i + batch_size]
            batch_metas = metadatas[i:i + batch_size]

            collection.add(
                ids=batch_ids,
                documents=batch_docs,
                metadatas=batch_metas
            )
    except Exception as e:
        print('________SAVE ERROR_____', e)
        return 'save error!'

    return f'vector count = {collection.count()}'


async def search(
        request: SearchRequest,
        encoding_model: str = Query('openai', enum=('gigachat', 'local_all_12', 'openai')),
        n_results: int = Query(10),
        include_embeddings: bool = Query(False),
):
    if encoding_model == 'openai':
        collection = openai_collection
    elif encoding_model == 'gigachat':
        collection = gigachat_collection
    else:
        return 'not valid encoding_model'

    include = ["metadatas", "documents", "distances"] + (["embeddings"] if include_embeddings else [])

    return collection.query(
        query_texts=request.text,
        # query_embeddings=gigachat_embedding_function([request.text]),
        n_results=n_results,
        include=include,
    )


async def top_chunks(
        encoding_model: str = Query('openai', enum=('gigachat', 'local_all_12', 'openai')),
        n_results: int = Query(10),
        offset: int = Query(0),
        include_embeddings: bool = Query(False)):
    if encoding_model == 'openai':
        collection = openai_collection
    elif encoding_model == 'gigachat':
        collection = gigachat_collection
    else:
        return 'not valid encoding_model'

    ids = [str(i) for i in range(offset, n_results + offset)]
    res = collection.get(ids=ids,
                         include=["metadatas", "documents"] + (["embeddings"] if include_embeddings else []))
    return res


async def get_collection_size( encoding_model: str = Query('openai', enum=('gigachat', 'local_all_12', 'openai'))):
    if encoding_model == 'openai':
        collection = openai_collection
    elif encoding_model == 'gigachat':
        collection = gigachat_collection
    else:
        return 0
    return collection.count()
