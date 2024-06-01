from typing import List, Dict

from fastapi import Query
from pydantic import BaseModel


class EmbeddingRequest(BaseModel):
    id: str
    text: str


class SearchRequest(BaseModel):
    text: str


class MetaDataQuestion(BaseModel):
    url: str = None
    source: str = None
    business_line_id: str = None
    direction: str = None
    product: str = None
    type: str = None
    description:str = None
    parent_title: str = None
    parent_url: str = None


class MetaDataFullText(BaseModel):
    title: str = None
    url: str = None
    source: str = None
    business_line_id: str = None
    direction: str = None
    product: str = None
    type: str = None
    description: str = None
    parent_title: str = None
    parent_url: str = None


class SaveDataRequest(BaseModel):
    encoding_model: str = Query('gigachat', enum=('gigachat', 'local_all_12', 'openai'))
    documents: List[str]
    metadatas: List[Dict]
