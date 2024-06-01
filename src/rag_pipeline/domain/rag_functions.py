import asyncio
from typing import List

from fastapi import Query

from embeddings.api.schema import SearchRequest
from embeddings.domain.chroma_utils import search
from llm.domain.gigachat_utils import rag_prompt

async def rag_db_response(request: SearchRequest,
                          encoding_model: str = Query('openai', enum=('gigachat', 'local_all_12', 'openai')),
                          n_results: int = Query(10),
                          include_embeddings: bool = Query(False),
                          ids: List[str] = Query([], alias="id"), ):
    results = await search(request, encoding_model, n_results, include_embeddings, ids)

    return results


async def rag_final_response(request: SearchRequest,
                             encoding_model: str = Query('openai', enum=('gigachat', 'local_all_12', 'openai')),
                             n_results: int = Query(10),
                             include_embeddings: bool = Query(False),
                             ids: List[str] = Query([], alias="id"), ):
    results = await search(request, encoding_model, n_results, include_embeddings, ids)

    context = ''

    for question, meta in zip(results['documents'][0], results['metadatas'][0]):

        context += f"\n Вопрос : {question}, \n Ответ : {meta['answer']}"

    output = await rag_prompt(request.text, context)

    return output, context
