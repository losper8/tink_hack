import html
import json
import os
import re
from urllib.parse import urljoin

from bs4 import BeautifulSoup

# Define the base URL
BASE_URL = 'https://www.tinkoff.ru'


def extract_text_with_links(element):
    if element.name == 'a':
        href = element["href"]
        full_url = urljoin(BASE_URL, href)
        return f'{element.get_text()} ({full_url})'
    if element.name == 'li':
        return '- ' + ''.join([extract_text_with_links(child) for child in element.children])
    if element.name in ['span', 'p', 'div']:
        return ''.join([extract_text_with_links(child) if child.name else child for child in element.children])
    return ''.join([extract_text_with_links(child) if child.name else child for child in element.children])


def extract_and_return_structured_text(element):
    if element.name == 'p':
        return extract_text_with_links(element) + '\n'
    elif element.name == 'ul':
        list_items = ''.join([extract_text_with_links(li) + '\n' for li in element.find_all('li')])
        return list_items + '\n'
    elif element.name == 'table':
        return extract_table(element)
    elif element.name == 'div':
        return extract_div(element)
    else:
        return extract_text_with_links(element)


def extract_table(table):
    rows = table.find_all('tr')
    header = [extract_text_with_links(th).strip() for th in rows[0].find_all('th')]
    table_text = ""
    for row in rows[1:]:
        columns = row.find_all(['th', 'td'])
        row_text = " ".join([extract_text_with_links(col).strip() for col in columns])
        table_text += row_text + '\n'
    return table_text + '\n'


def extract_div(div):
    div_text = ""
    if 'data-testid' in div.attrs and div['data-testid'] == 'indented-block':
        div_text += extract_indented_blocks(div)
    else:
        for child in div.children:
            if child.name:
                div_text += extract_and_return_structured_text(child)
    return div_text


def extract_indented_blocks(div):
    blocks = div.find_all('div', recursive=False)
    block_text = ""
    for block in blocks:
        if 'data-testid' in block.attrs and block['data-testid'] == 'indented-block':
            block_text += extract_indented_blocks(block)
        else:
            block_text += '\t'.join([extract_text_with_links(inner_block).strip() for inner_block in block.find_all('div', recursive=False)]) + '\n'
    return block_text


def clean_text(text):
    text = text.replace('\xa0', ' ')
    text = html.unescape(text)
    text = text.replace('\u2060', '')
    return text


def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '', filename)


def format_question_answer(text):
    lines = text.strip().split('\n')
    if len(lines) > 0 and '?' in lines[0]:
        question, answer = lines[0].split('?', 1)
        question = question.strip() + '?'
        answer = answer.strip()
        return question + '\n' + answer + '\n' + '\n'.join(lines[1:])
    return text


def main():
    html_dir = 'data/html'
    parsed_dir = 'data/parsed'
    files_list = os.listdir(html_dir)
    empty_files = []
    strange_names = []
    for file in files_list:
        file_url = 'https://www.tinkoff.ru/' + file.replace('_', '/').replace('.html', '')

        print(f'{file_url=}')
        with open(f'{html_dir}/{file}', encoding='utf-8') as f:
            html_content = f.read()
        bs4 = BeautifulSoup(html_content, 'html.parser')

        articles = bs4.find_all('article')
        print(f'{len(articles)=}')

        # table_of_content = bs4.find('div', {'data-testid': 'table-of-content'})
        # len_table_of_content_lis = 0
        # if table_of_content:
        #     table_of_content_lis = table_of_content.find_all('li')
        #     len_table_of_content_lis = len(table_of_content_lis)
        # print(f'{len_table_of_content_lis=}')

        if not articles:
            empty_files.append({'file': file, 'url': file_url})
            continue

        dir_name = file.replace('.html', '')
        dir_path = os.path.join(parsed_dir, dir_name)
        os.makedirs(dir_path, exist_ok=True)

        for i, article in enumerate(articles):
            text_output = ""
            for child in article.children:
                if child.name:
                    text_output += extract_and_return_structured_text(child)
            text_output = clean_text(text_output)
            text_output = format_question_answer(text_output)
            question = text_output.split('\n')[0]
            if '?' not in question:
                question += '?'

            sanitized_question = sanitize_filename(question)
            output_file_path = os.path.join(dir_path, f'{sanitized_question}.txt')
            try:
                with open(output_file_path, 'w', encoding='utf-8') as out_file:
                    out_file.write(text_output)
            except OSError:
                strange_names.append({'file': file, 'url': file_url, 'question': question})

    with open('data/empty_files.json', 'w', encoding='utf-8') as f:
        json.dump(empty_files, f, indent=4, ensure_ascii=False)
    with open('data/strange_names.json', 'w', encoding='utf-8') as f:
        json.dump(strange_names, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    main()
