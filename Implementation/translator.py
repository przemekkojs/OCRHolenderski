import asyncio

from languages import check_if_language_exists
from googletrans import Translator
from paths import get_phrase_from_dictionary, set_phrase_to_dictionary
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from complex_types import row, buffer_row

model_name = "facebook/nllb-200-distilled-600M"
_tokenizer = AutoTokenizer.from_pretrained(model_name)
_model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
_translator = pipeline("translation", model=_model, tokenizer=_tokenizer, src_lang="nld_Latn", tgt_lang="pol_Latn")

async def __translate_word_api(what:str, lang_from:str, buffer:list[buffer_row], lang_to:str='pl', debug:bool=False) -> str:
    if debug:
        print(f"Tłumaczenie {what} z >> {lang_from} << na >> {lang_to} <<")

    if what == "":
        return ""
    
    if not check_if_language_exists(lang_from):
        raise ValueError(f"Language {lang_from} is not supported")   

    dictionary_translation:str = await get_phrase_from_dictionary(what, lang_from, lang_to)

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
        buffer.append(buffer_row(
            word=what,
            translation=text
        ))

        return text

async def __translate_word_model(what:str, lang_from:str, buffer:list[buffer_row], lang_to:str='pl', debug:bool=False) -> str:
    if debug:
        print(f"Tłumaczenie {what} z >> {lang_from} << na >> {lang_to} << z użyciem modelu >> {model_name} <<")

    if what == "":
        return ""

    if not check_if_language_exists(lang_from):
        raise ValueError(f"Language {lang_from} is not supported")    

    dictionary_translation:str = await get_phrase_from_dictionary(what, lang_from, lang_to)

    if dictionary_translation != "":
        if debug:
            print("Tłumaczenie znalezione w słowniku")

        return dictionary_translation
    else:
        if debug:
            print("Tłumaczenie z użyciem modelu")

        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(None, lambda: _translator(what)[0]["translation_text"])

        buffer.append(buffer_row(
            word=what,
            translation=result
        ))

        return result

def create_full_sentences(input:list[row], lang:str, debug:bool=False) -> list[row]:
    input.sort(key=lambda x:(x.coords[2], x.coords[0]))
    result:list[row] = []    

    return result

async def translate(input: list[row], lang_from:str, lang_to:str='pl', translation_mode:str='api') -> None:
    __translation_buffer:list[buffer_row] = []
    tasks:list = []

    if translation_mode not in ['model', 'api']:
        raise ValueError("Possible translation modes are 'model' and 'api'")

    for current_row in input:
        word:str = current_row.word
        translation_func:function = __translate_word_model if translation_mode == 'model' else __translate_word_api
        tasks.append(translation_func(word, lang_from, buffer=__translation_buffer, lang_to=lang_to))

    results: list[str | Exception] = await asyncio.gather(*tasks, return_exceptions=True)

    for index in range(len(results)):
        result = results[index]
        current:row = input[index]

        if isinstance(result, Exception):
            print(str(result))
            current.translation = "NIEPOWODZENIE"
        else:
            current.translation = result

    for words in __translation_buffer:
        await set_phrase_to_dictionary(words.word, words.translation, lang_from, lang_to)
