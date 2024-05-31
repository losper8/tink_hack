from time import perf_counter

import requests
import tqdm

cookies = {
    'test_cookie_QpHfCYJQhs': 'true',
    '__P__wuid': '50ea731e02763495ad16c247bab63363',
    'rid': '77',
    'dco.id': 'f175177b-34d0-44a6-961f-00006ef25e3a',
    'userType': 'Visitor',
    'stDeIdU': '50ea731e02763495ad16c247bab63363',
    'dsp_click_id': 'no%20dsp_click_id',
    'pageLanding': 'https%3A%2F%2Fwww.tinkoff.ru%2Fbusiness%2Fhelp%2F',
    '__P__wuid_last_update_time': '1717139244496',
    'tmr_lvid': 'f3ab8d4410e97cfbe603f10bb115a792',
    'tmr_lvidTS': '1717139244908',
    'uxs_uid': '6ed0fcb0-1f1c-11ef-9cd1-25574aa0252d',
    '_ym_uid': '1717139246123708627',
    '_ym_d': '1717139246',
    '_ym_isad': '1',
    '_ymab_param': 'XP0jy9ViKeUSDJTMYK3Kg8HYLan16jEn915cbUDpB8u1CdutB20NBJyWmuo5NUUWOAzm2cp9jeitR7h3R9CvUhAzUBI',
    '_t_modern': 'true',
    'tmr_detect': '1%7C1717139557849',
    '__P__wuid_visit_id': 'v1%3A0000002%3A1717142474203%3A50ea731e02763495ad16c247bab63363',
    '__P__wuid_visit_persistence': '1717142474203',
    'vIdUid': 'ca635a26-bfca-4814-9126-6ae00f96abf7',
    'stSeStTi': '1717142474212',
    'psid': '9JFm2YquhJjGtK1ixHZWaF6n8VbIbZnP.ds-prod-api-140',
    '_ym_visorc': 'b',
    'mediaInfo': '{%22width%22:1044%2C%22height%22:413%2C%22isTouch%22:false%2C%22displayMode%22:%22browser%22%2C%22retina%22:true}',
    'stLaEvTi': '1717145122512',
    'tmr_reqNum': '46',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'dnt': '1',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-arch': '"arm"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"macOS"',
    'sec-ch-ua-platform-version': '"14.5.0"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
}

with open('data/parent_urls.txt') as f:
    urls = f.readlines()
urls = [url.strip() for url in urls]
print(f'{len(urls)=}')
for url in tqdm.tqdm(urls):
    # print(f'{url=}')
    start = perf_counter()
    response = requests.get(
        url,
        headers=headers,
    )

    if url.endswith('/'):
        url = url[:-1]
    url_file_name = url.replace('https://www.tinkoff.ru/', '').replace('/', '_')

    response.encoding = 'utf-8'

    with open(f'data/html/{url_file_name}.html', 'w', encoding='utf-8') as f:
        f.write(response.text)
    # print(f'{perf_counter() - start=}')
