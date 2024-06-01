import asyncio
import json
import re

BASE_URL = 'https://www.tinkoff.ru'


def extract_links(text):
    # Regex to match Markdown-style links and embedded images
    link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    image_pattern = r'!\[\]\(([^)]+)\)'

    links = re.findall(link_pattern, text)

    images = re.findall(image_pattern, text)

    extracted_links = {link[0]: link[1] for link in links}

    for extracted_links_key in extracted_links.keys():
        if not extracted_links[extracted_links_key].startswith('http') and BASE_URL not in extracted_links[extracted_links_key]:
            extracted_links[extracted_links_key] = BASE_URL + extracted_links[extracted_links_key]
    image_links = {f'image {i + 1}': img for i, img in enumerate(images)}

    return extracted_links, image_links


def remove_links(text):
    link_pattern = r'\[([^\]]+)\]\([^)]+\)'
    image_pattern = r'!\[\]\(([^)]+)\)'

    text_without_links = re.sub(link_pattern, r'\1', text)
    text_without_images = re.sub(image_pattern, '', text_without_links)

    return text_without_images


async def main():
    with open('../data/norm_dataset_clean_with_uuid_and_questions.json') as f:
        data = json.load(f)

    for item in data:
        answer = item.get('answer', '')
        links, image_links = extract_links(answer)
        cleaned_answer = remove_links(answer)

        item['links'] = links
        item['image_links'] = image_links
        item['cleaned_answer'] = cleaned_answer

        url = item['url']
        if not url.startswith(BASE_URL):
            item['url'] = BASE_URL + url

    with open('../data/final_norm_dataset.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    asyncio.run(main())
