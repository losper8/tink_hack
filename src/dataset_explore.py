import asyncio
import json

import pandas as pd


async def main():
    with open('data/dataset.json') as f:
        data = json.load(f)['data']
    print(len(data))

    df = pd.DataFrame(data)

    is_unique_ids = df['id'].is_unique
    print(f"{is_unique_ids=}")

    description_counts = df['description'].value_counts()
    most_frequent_descriptions = description_counts.head()
    print(most_frequent_descriptions)

    parent_urls = df['parent_url'].unique()
    urls = df['url']
    urls = [url.split('?')[0] for url in urls]
    urls = set(urls)
    parent_urls = [url for url in parent_urls if url] + list(urls)
    parent_urls = list(set(parent_urls))
    print(parent_urls)
    print(len(parent_urls))
    parent_url_lines = [f"{url}\n" for url in parent_urls]

    with open('data/parent_urls.txt', 'w') as f:
        f.writelines(parent_url_lines)


if __name__ == '__main__':
    asyncio.run(main())
