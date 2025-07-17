import asyncio

from languages import check_if_language_exists
from googletrans import Translator
from paths import get_phrase_from_dictionary, set_phrase_to_dictionary

async def translate_word(what:str, lang_from:str, buffer:list[tuple[str, str]], lang_to:str='pl', debug:bool=False) -> str:
    if what == "":
        return ""
    if not check_if_language_exists(lang_from):
        raise ValueError(f"Language {lang_from} is not supported")

    if debug:
        print(f"Tłumaczenie {what} z >> {lang_from} << na >> {lang_to} <<")

    dictionary_translation = await get_phrase_from_dictionary(what, lang_from, lang_to)

    if dictionary_translation != "":
        if debug:
            print("Tłumaczenie znalezione w słowniku")

        return dictionary_translation
    else:
        if debug:
            print("Tłumaczenie z użyciem API")

        translator = Translator()
        result = await translator.translate(what, dest=lang_to, src=lang_from)
        text = result.text
        buffer.append((what, text))

        return text

async def translate(input: list[list[str | list]], lang_from:str, lang_to:str='pl') -> None:
    __translation_buffer = []
    tasks:list = []

    for row in input:
        word = row[0]
        tasks.append(translate_word(word, lang_from, buffer=__translation_buffer, lang_to=lang_to))

    results: list[str | Exception] = await asyncio.gather(*tasks, return_exceptions=True)

    for index in range(len(results)):
        result = results[index]
        current:list[str | list] = input[index]

        if isinstance(result, Exception):
            print(str(result))
            current.append("NIEPOWODZENIE")
        else:
            current.append(result)

    for words in __translation_buffer:
        phrase:str = words[0]
        translation:str = words[1]
        await set_phrase_to_dictionary(phrase, translation, lang_from, lang_to)