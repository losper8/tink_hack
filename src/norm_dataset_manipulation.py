import asyncio
import json

import pandas as pd


async def main():
    with open('../data/norm_dataset.json') as f:
        data = json.load(f)
    print(len(data))

    df = pd.DataFrame(data)

    print(df.head())

    question_counts = df['question'].value_counts()
    print(question_counts.head(150))


if __name__ == '__main__':
    asyncio.run(main())
