import json
import pandas as pd

from embeddings.api.schema import MetaDataQuestion, SaveDataRequest


async def data_to_save_request(encoding_model: str = 'openai', path: str = '../../tinkoff_data/dataset.json'):
    with open(path, encoding='utf-8') as f:
        data = json.load(f)['data']

    df = pd.DataFrame(data)

    documents = []
    metadatas = []

    for index, item in df.iterrows():
        question = item.loc['title'][:5000]
        data_item = MetaDataQuestion(
            url=item.loc['url'],
            source=item.loc['source'],
            business_line_id=item.loc['business_line_id'],
            direction=item.loc['direction'],
            product=item.loc['product'],
            type=item.loc['type'],
            description=item.loc['description'],
            parent_title=item.loc['parent_title'],
            parent_url=item.loc['parent_url'],
        )
        documents.append(question)

        metadatas.append(data_item.__dict__)

    return SaveDataRequest(encoding_model=encoding_model, documents=documents, metadatas=metadatas)


if __name__ == '__main__':
    r = data_to_save_request()
    print(r)
