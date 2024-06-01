import asyncio
import json
import os
from time import perf_counter

import aiofiles
import openai
from tenacity import (
    retry,
    wait_random_exponential,
)

openai_client = openai.AsyncClient(
    api_key='sk-proj-763tkhP5oJ85hr0Ir0jmT3BlbkFJO294dhYqZcPdYzQXMgJn'
)


# @retry(
#     wait=wait_random_exponential(min=1, max=4),
# )
async def augment_query_generated(semaphore, uuid, breadcrumps, answer, model="gpt-3.5-turbo"):
    async with semaphore:
        start = perf_counter()
        messages = [
            {
                "role": "system",
                "content": "Используя следующие данные, включающие контекст (хлебные крошки) и текст ответа, извлеките все возможные вопросы, которые будут полезны для новых и текущих пользователей (предпринимателей). Контекст хлебных крошек указывает на категорию и подкатегорию информации, поэтому каждый вопрос должен соответствовать указанному контексту.\nЗадача: Извлеките все возможные вопросы из текста ответа, учитывая контекст. Обеспечьте, чтобы каждый вопрос был релевантен категории и подкатегории, указанной в хлебных крошках. Сформулируйте вопросы четко и лаконично."
            },
            {
                "role": "user",
                "content": f"Данные:\nКонтекст: {breadcrumps}\nОтвет: {answer}\n"
            }
        ]

        response = await openai_client.chat.completions.create(
            model=model,
            messages=messages,
        )
        content = response.choices[0].message.content

        async with aiofiles.open(f'../data/questions/{uuid}.txt', 'w') as f:
            await f.write(content)

        print(response)
        print(content)
        print(f"Processed {uuid} in {perf_counter() - start:.2f} seconds")
        return content


async def main():
    model = "gpt-4o"
    max_concurrent_requests = 10
    semaphore = asyncio.Semaphore(max_concurrent_requests)

    with open('../data/norm_dataset_clean_with_uuid.json') as f:
        data = json.load(f)
    print(len(data))

    already_saved_ids = [file.replace('.txt', '') for file in os.listdir('../data/questions')]
    print(f'{len(already_saved_ids)=}')

    tasks = []
    for item in data:
        if item['id'] in already_saved_ids:
            print(f"Skipping {item['id']} as it is already processed")
            continue
        if not item['breadcrumps']:
            print(f"Skipping {item['id']} due to missing breadcrumps")
            continue
        tasks.append(augment_query_generated(semaphore, item['id'], item['breadcrumps'], item['answer'], model))

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
