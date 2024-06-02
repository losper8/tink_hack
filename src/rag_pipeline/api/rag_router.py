from typing import List
from fastapi import APIRouter, Query

from embeddings.api.schema import SearchRequest
from rag_pipeline.domain.rag_functions import rag_db_response, rag_final_response
from rag_pipeline.domain.rag_utils import fill_rag_db

rag_router = APIRouter(
    prefix="",
    tags=["default"],
)

@rag_router.post(
    "/assist",
)
async def Assist(
        request: SearchRequest
):
    res = await rag_final_response(request, encoding_model='openai', n_results=3, include_embeddings=False)
    return res


