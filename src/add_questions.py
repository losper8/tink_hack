import asyncio
import json

import aiofiles
from tqdm import tqdm


async def main():
    with open('../data/norm_dataset_clean_with_uuid.json') as f:
        data = json.load(f)
    for item in tqdm(data):
        id_ = item['id']
        breadcrumbs = item['breadcrumps']
        question = item['question']
        original_question_set = set([question])
        if not breadcrumbs:
            continue
        # question = item['question']
        async with aiofiles.open(f'../data/questions_openai/{id_}.txt', 'r') as f:
            content = await f.read()
            questions_openai = content.split('\n')
            questions_openai_set = set(questions_openai)
            unique_openai_questions = questions_openai_set - original_question_set
            questions_openai = list(unique_openai_questions)
            item['openai_questions'] = questions_openai

        async with aiofiles.open(f'../data/questions_yandex/{id_}.txt', 'r') as f:
            content = await f.read()
            questions_yandex = content.split('\n')
            questions_yandex_set = set(questions_yandex)
            unique_yandex_questions = questions_yandex_set - questions_openai_set
            questions_yandex = list(unique_yandex_questions)
            item['yandex_questions'] = questions_yandex
    with open('../data/norm_dataset_clean_with_uuid_and_questions.json', 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    asyncio.run(main())
