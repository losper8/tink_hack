from cleantext import clean

def ru_embedding_clean(text, **kwargs):
    args = {
        'fix_unicode': True,
        'to_ascii': False,
        'lower': True,
        'normalize_whitespace': True,
        'no_line_breaks': True,
        'strip_lines': True,
        'keep_two_line_breaks': False,
        'no_urls': True,
        'no_emails': True,
        'no_phone_numbers': True,
        'no_numbers': False,
        'no_digits': False,
        'no_currency_symbols': True,
        'no_punct': False,
        'no_emoji': True,
        'replace_with_url': "<ссылка>",
        'replace_with_email': "<почта>",
        'replace_with_phone_number': "<телефон>",
        'replace_with_number': "",
        'replace_with_digit': "",
        'replace_with_currency_symbol': "<валюта>",
        'replace_with_punct': "",
        'lang': "ru",
    }

    for key in kwargs:
        if key not in args:
            raise ValueError(f"Недопустимый аргумент: {key}")

    args.update(kwargs)
    return clean(text, **args)


def en_embedding_clean(text, **kwargs):
    args = {
        'fix_unicode': True,
        'to_ascii': False,
        'lower': True,
        'normalize_whitespace': True,
        'no_line_breaks': True,
        'strip_lines': True,
        'keep_two_line_breaks': False,
        'no_urls': True,
        'no_emails': True,
        'no_phone_numbers': True,
        'no_numbers': False,
        'no_digits': False,
        'no_currency_symbols': True,
        'no_punct': False,
        'no_emoji': True,
        'replace_with_url': "<URL>",
        'replace_with_email': "<EMAIL>",
        'replace_with_phone_number': "<PHONE>",
        'replace_with_number': "",
        'replace_with_digit': "",
        'replace_with_currency_symbol': "<CUR>",
        'replace_with_punct': "",
        'lang': "en",
    }

    for key in kwargs:
        if key not in args:
            raise ValueError(f"Недопустимый аргумент: {key}")

    args.update(kwargs)
    return clean(text, **args)


