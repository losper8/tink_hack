import json
import os
import pandas as pd

from embeddings.api.schema import SaveDataRequest

data = pd.read_json('/opt/app-root/questions/norm_dataset_clean_with_uuid.json')
print('-------------------------->>>>>',data.head())


def get_breadcrumps(uuid: str):
    df_filtered = data[data['id'] == uuid]
    breadcrumps = ''
    if not df_filtered.empty:
        breadcrumps = df_filtered['breadcrumps'].values[0]
    else:
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', uuid)
    return breadcrumps


async def get_urls(uuid: str):
    df_filtered = data[data['id'] == uuid]
    parent_url = df_filtered['parent_url'].values[0]
    url = df_filtered['url'].values[0]
    url = r"https://www.tinkoff.ru" + url
    return url, parent_url


async def get_answer(uuid: str):
    df_filtered = data[data['id'] == uuid]
    answer = df_filtered['answer'].values[0]
    return answer


async def txt_files_to_save_request(encoding_model: str = 'openai', directory: str = ''):
    documents = []
    metadatas = []
    for z, filename in enumerate(os.listdir(directory)):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                sentences = [sentence.strip() for sentence in content.split('\n')]
                sentences = [get_breadcrumps(filename[:-4]) + s for s in sentences]  # add breadcrumps
                meta = [{'uuid': filename[:-4]} for _ in sentences]
                documents += sentences
                metadatas += meta

    return SaveDataRequest(encoding_model=encoding_model, documents=documents, metadatas=metadatas)
