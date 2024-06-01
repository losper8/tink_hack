import asyncio
import json


async def main():
    with open('../data/norm_dataset_clean_with_uuid.json') as f:
        data = json.load(f)
    breadcrumbs = set()
    for item in data:
        # id_ = item['id']
        breadcrumbs_line = item['breadcrumps']
        if not breadcrumbs_line:
            continue
        breadcrumbs_ = breadcrumbs_line.split(' > ')
        breadcrumbs.update(breadcrumbs_)
    breadcrumbs = list(sorted(breadcrumbs))
    print(f"{len(breadcrumbs)=}")
    for breadcrumb in breadcrumbs:
        print(breadcrumb)


if __name__ == '__main__':
    asyncio.run(main())
