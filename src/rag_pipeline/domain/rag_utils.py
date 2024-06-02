import asyncio
from typing import List

from fastapi import Query
from langchain_text_splitters import split_text_on_tokens

from embeddings.api.schema import SearchRequest, SaveDataRequest
from embeddings.domain.chroma_utils import search, add_vectors_to_db, get_collection_size

from file_processing.data_proccessing import save_json_to_db
from file_processing.text_cleaners.cleaning import en_embedding_clean
from file_processing.text_splitters.ru_token_splitter import RU_TOKEN_SPLITTER


async def fill_rag_db(encoding_model: str = Query('openai', enum=('gigachat', 'local_all_12', 'openai'))):
    current_size = await get_collection_size(encoding_model)
    if current_size == 0:
        file_path = '/opt/app-root/final_data_schema/final_norm_dataset.json'
        request = await save_json_to_db(encoding_model, file_path)
        return await add_vectors_to_db(request)
    return f'already filled or no such collection {current_size}'

