import asyncio

from languages import check_if_language_exists
from googletrans import Translator

# Wsm to zaimplementować i reszta działa
async def translate_word(what:str, lang_from:str, lang_to:str='pl', debug:bool=False) -> str:
    if what == "":
        return ""

    if not check_if_language_exists(lang_from):
        raise ValueError(f"Language {lang_from} is not supported")    

    if debug:
        print(f"Tłumaczenie {what} z >> {lang_from} << na >> {lang_to} <<")

    translator = Translator()
    result = await translator.translate(what, dest=lang_to, src=lang_from)

    return result.text

async def translate(input: list[list[str | list]], lang_from:str, lang_to:str='pl') -> None:
    tasks:list = []

    for row in input:
        word = row[0]
        tasks.append(translate_word(word, lang_from, lang_to))

    results: list[str | Exception] = await asyncio.gather(*tasks, return_exceptions=True)

    for index in range(len(results)):
        result = results[index]
        current:list[str | list] = input[index]

        if isinstance(result, Exception):
            current.append("NIEPOWODZENIE")
        else:
            current.append(result)
