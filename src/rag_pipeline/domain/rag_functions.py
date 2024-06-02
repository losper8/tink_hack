import asyncio
from typing import List

from fastapi import Query

from embeddings.api.schema import SearchRequest
from embeddings.domain.chroma_utils import search
from llm.domain.gigachat_utils import rag_prompt

async def rag_db_response(request: SearchRequest,
                          encoding_model: str = Query('openai', enum=('gigachat', 'local_all_12', 'openai')),
                          n_results: int = Query(10),
                          include_embeddings: bool = Query(False), ):
    results = await search(request, encoding_model, n_results, include_embeddings)

    return results


async def rag_final_response(request: SearchRequest,
                             encoding_model: str = Query('openai', enum=('gigachat', 'local_all_12', 'openai')),
                             n_results: int = Query(10),
                             include_embeddings: bool = Query(False),):

    if request.text == '':
        r = {
            'text': '',
            'links': []
        }
        return r

    results = await search(request, encoding_model, n_results, include_embeddings)

    context = ''

    for question, meta in zip(results['documents'][0], results['metadatas'][0]):

        context += f"\n Вопрос : {question.split('>')[-1]}, \n Ответ : {meta['answer']}"

    output = await rag_prompt(request.text, context[:5000])

    links = [p['url'] for p in results['metadatas'][0]]

    r = {
        'text': output.replace('\n', ' ').replace('*', ' '),
        'links': links
    }

    return r
