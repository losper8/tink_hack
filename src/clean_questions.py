import asyncio
import os
import re

import aiofiles


async def main():
    questions_dir = '../data/questions_yandex'

    files = os.listdir(questions_dir)

    # for file in tqdm.tqdm(files):
    for file in files:
        async with aiofiles.open(f'{questions_dir}/{file}', 'r') as f:
            content = await f.read()
            content = re.sub(r'\n{2,}', '\n', content)
            result = []
            for line in content.splitlines():
                line_clean = line.lower().strip()
                if not line_clean:
                    continue
                # if 'вопрос' in line_clean or 'контекст' in line_clean or 'помощь > бизнес' in line_clean or 'категория: **' in line_clean or "помощь > банк" in line_clean:
                #     continue
                if 'вопрос' in line_clean:
                    continue

                # print(f'{line}')
                if '?' not in line:
                    # print(f'{line=}')
                    # print(f'{file=}')
                    print(line)
                    print(file)
                    print()
                # result.append(line)
                # 6. Пример расчета налога по УСН «Доходы» с доходов в валюте.
                # remove digits with dot at start:
                if re.match(r'^\d+\.', line):
                    line = re.sub(r'^\d+\.', '', line)
                line = line.replace('*', '')
                line = line.strip()
                result.append(line)
            content = '\n'.join(result)
        async with aiofiles.open(f'{questions_dir}/{file}', 'w') as f:
            await f.write(content)


if __name__ == '__main__':
    asyncio.run(main())
