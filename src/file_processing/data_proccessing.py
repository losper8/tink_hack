import json
import os
import pandas as pd
from embeddings.api.schema import SaveDataRequest


async def save_json_to_db(encoding_model: str='openai', path: str = 'final_data_schema/final_norm_dataset.json'):
    data = pd.read_json(path)

    documents = []
    metadatas = []

    for index, row in data.iterrows():
        url = row.loc['url']
        parent_url = row.loc['parent_url']
        breadcrumps = row.loc['breadcrumps']
        q = row.loc['question']
        answer = row.loc['cleaned_answer']
        uuid = row.loc['id']
        links = row.loc['links']
        image_links = row.loc['image_links']
        o_q = row.loc['openai_questions']
        y_q = row.loc['yandex_questions']
        questions = [q]

        if isinstance(o_q, list):
            questions += o_q

        if isinstance(y_q, list):
            questions += y_q

        docs = [breadcrumps + que for que in questions]
        meta = {
            'url': url,
            'parent_url': parent_url,
            'answer': answer,
            'uuid': uuid,
            #'links': links,
            #'image_links': image_links
        }
        metas = [meta.copy() for _ in docs]
        documents += docs
        metadatas += metas
        print(metadatas[0])
    return SaveDataRequest(encoding_model=encoding_model, documents=documents, metadatas=metadatas)