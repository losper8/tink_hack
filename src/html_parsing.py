import json
import os
import re

import html2text
import lxml.html
import lxml.html.clean
from bs4 import BeautifulSoup

BASE_URL = 'https://www.tinkoff.ru'

_RE_COMBINE_WHITESPACE = re.compile(r"\s+")

h = html2text.HTML2Text()
h.skip_internal_links = False
h.single_line_break = True
h.ignore_links = False
h.ignore_images = False
h.inline_links = True
h.protect_links = False
h.ignore_emphasis = True
h.mark_code = False
h.body_width = 0
h.google_list_indent = 0
h.bypass_tables = True
# h.ignore_tables = True
h.wrap_tables = True

h.ignore_anchors = True


def clean_text(text):
    doc = lxml.html.fromstring(text)
    cleaner = lxml.html.clean.Cleaner(style=True)
    doc = cleaner.clean_html(doc)
    text = doc.text_content()
    text = text.replace('⁠', '')
    text = text.replace('​', '')
    return text


def sanitize_filename(filename):
    filename = clean_text(filename)
    return re.sub(r'[<>:"/\\|?*]', '', filename)


def html_table_to_markdown(table):
    rows = table.find_all('tr')
    headers = rows[0].find_all(['th', 'td'])
    header_row = '| ' + ' | '.join([header.get_text(strip=True) for header in headers]) + ' |'

    markdown_table = [header_row]

    for row in rows[1:]:
        cols = row.find_all(['td', 'th'])
        markdown_row = '| ' + ' | '.join([col.get_text(strip=True) for col in cols]) + ' |'
        markdown_table.append(markdown_row)

    return '\n'.join(markdown_table)


def replace_tables_with_markdown(text):
    # bs4 = BeautifulSoup(text, 'html.parser')
    # tables = bs4.find_all('table')
    #
    # for table in tables:
    #     markdown_table = html_table_to_markdown(table)
    #     table.replace_with(markdown_table)
    #
    # return str(bs4)

    # replace all between <table> and </table> with empty
    return re.sub(r'<table.*?>.*?</table>', '', text, flags=re.DOTALL)


def remove_any_html_related_encodig_from_text(text):
    text = text.replace('&nbsp;', ' ')
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
            # data_url_href_element = article.find('h2', {'data-url': True})
            # deta_url_href = data_url_href_element['data-url'] if data_url_href_element else None
            # deta_url_href = urllib.parse.unquote(deta_url_href) if deta_url_href else None
            # print(f'{deta_url_href=}')

            text_output = h.handle(str(article))
            text_output = replace_tables_with_markdown(text_output)
            # print(f'{text_output=}')

            # text_output = ""
            # for child in article.children:
            #     if child.name:
            #         text_output += extract_and_return_structured_text(child)
            # text_output = clean_text(text_output)
            # text_output = format_question_answer(text_output)

            question = text_output.split('\n')[0].replace('#', '').replace('\n', ' ').strip()
            if '?' not in question:
                question += '?'
            if question.startswith('Как работать с депозитом: настраивать, пополнять и снимать деньгиНастроить депозит'):
                question = 'Как работать с депозитом: настраивать, пополнять и снимать деньги?'
            elif question.startswith('Зачем проверять контрагентовФНС'):
                question = 'Зачем проверять контрагентов?'
            if question == 'card?':
                continue

            sanitized_question = sanitize_filename(question)
            output_file_path = os.path.join(dir_path, f'{sanitized_question}.txt')
            try:
                with open(output_file_path, 'w', encoding='utf-8') as out_file:
                    # text_output = '\n'.join([line.strip() for line in text_output.split('\n')])
                    text_output = re.sub(r'\n{2,}', '\n', text_output)
                    # # text_output = '\n'.join([line.strip() for line in text_output.split('\n')])
                    text_output = '\n'.join([_RE_COMBINE_WHITESPACE.sub(" ", line).strip() for line in text_output.split('\n')])
                    # text_output = text_output.replace('-\n', '- ')
                    #
                    # text_output = text_output.replace(' .', '.')
                    # text_output = text_output.replace('. -', '.\n-')
                    text_output = clean_text(text_output)
                    out_file.write(text_output)
            except OSError:
                strange_names.append({'file': file, 'url': file_url, 'question': question})

    with open('data/empty_files.json', 'w', encoding='utf-8') as f:
        json.dump(empty_files, f, indent=4, ensure_ascii=False)
    with open('data/strange_names.json', 'w', encoding='utf-8') as f:
        json.dump(strange_names, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    main()
