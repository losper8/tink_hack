# -*- coding: utf8 -*-
from typing import List
from langchain_text_splitters import Tokenizer, split_text_on_tokens
from razdel import tokenize


def token_function(text: str) -> List[str]:
    tokens = list(tokenize(text))
    return [_.text for _ in tokens]


def local_tokenizer_length(text: str) -> int:
    # Assuming `tokenizer` is your local tokenizer instance
    return len(token_function(text))


def local_tokenizer_encode(text: str) -> list[str]:
    # Assuming `tokenizer` is your local tokenizer instance
    return token_function(text)


def local_tokenizer_decode(token_ids: List[str]) -> str:
    # Assuming `tokenizer` is your local tokenizer instance
    return ' '.join(token_ids)


class RU_TOKEN_SPLITTER(Tokenizer):
    def __init__(self, chunk_overlap: int, tokens_per_chunk):
        super().__init__(chunk_overlap=chunk_overlap,
                         tokens_per_chunk=tokens_per_chunk,
                         decode=local_tokenizer_decode,
                         encode=local_tokenizer_encode, )


text_splitter = RU_TOKEN_SPLITTER(chunk_overlap=2, tokens_per_chunk=5)

if __name__ == '__main__':
    test_text = "Feel no shame about shape! Weather changes? their phrase Even mother will show you another way So put your glasses on Nothing will be wrong There's no blame, there's no fame It's up to you"
    splits = split_text_on_tokens(text=test_text, tokenizer=text_splitter)
    print(splits)

    test_text = "Меня зовут Кира Йошикагэ. Мне 33 года. Мой дом находится в северо-восточной части Морио, в районе поместий. Работаю в офисе сети магазинов Kame Yu и домой возвращаюсь, самое позднее, в восемь вечера. Не курю, выпиваю изредка. Ложусь спать в 11 вечера и убеждаюсь, что получаю ровно восемь часов сна, несмотря ни на что. Перед сном я пью тёплое молоко, а также минут двадцать уделяю разминке, поэтому до утра сплю без особых проблем. Утром я просыпаюсь, не чувствуя ни усталости, ни стресса, словно младенец. На медосмотре мне сказали, что никаких проблем нет. Я пытаюсь донести, что я обычный человек, который хочет жить спокойной жизнью. Я не забиваю себе голову проблемами вроде побед или поражений, и не обзавожусь врагами, из-за которых не мог бы уснуть. Я знаю наверняка: в таком способе взаимодействия с обществом и кроется счастье. Хотя, если бы мне пришлось сражаться, я бы никому не проиграл."
    splits = split_text_on_tokens(text=test_text, tokenizer=text_splitter)
    print(splits)
