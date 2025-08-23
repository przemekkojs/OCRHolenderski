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

def __create_full_sentences(input:list[row], lang:str, debug:bool=False) -> list[row]:
    row_index:int = 0
    page_width:int = 1240

    while row_index < len(input) - 1:
        current_row:row = input[row_index]
        next_row:row = input[row_index + 1]        

        current_row_width:int = abs(current_row.rect[0] - current_row.rect[1])
        current_row_end_y:int = current_row.rect[3]
        next_row_start_y:int = next_row.rect[2]

        if current_row_width > 0.5 * page_width and current_row_end_y >= next_row_start_y - 3:
            input.pop(row_index + 1)
            next_row_width:int = abs(next_row.rect[0] - next_row.rect[1])
            y_override:int = next_row.rect[3]

            current_text:str = current_row.word
            next_text:str = next_row.word
            merged_text:str = f"{current_text}{next_text}"

            current_row.word = merged_text

            if current_row.rect[3] < y_override:
                current_row.rect[3] = y_override

            if current_row.rect[1] < next_row_width:
                current_row.rect[1] = next_row_width
        else:
            row_index += 1

    return input            

async def translate(input: list[row], lang_from:str, lang_to:str='pl', translation_mode:str='api', debug:bool=False) -> None:
    __translation_buffer:list[buffer_row] = []
    tasks:list = []

    if translation_mode not in ['model', 'api']:
        raise ValueError("Possible translation modes are 'model' and 'api'")
    
    sentences:list[row] = __create_full_sentences(input, lang_from, debug=debug)
    # sentences:list[row] = input

    for current_row in sentences:
        word:str = current_row.word
        translation_func:function = __translate_word_model if translation_mode == 'model' else __translate_word_api
        tasks.append(translation_func(word, lang_from, buffer=__translation_buffer, lang_to=lang_to))

    results: list[str | Exception] = await asyncio.gather(*tasks, return_exceptions=True)

    for index in range(len(results)):
        result = results[index]
        current:row = sentences[index]

        if isinstance(result, Exception):
            if debug:
                print(str(result))

            current.translation = ""
        else:
            current.translation = result

    for words in __translation_buffer:
        await set_phrase_to_dictionary(words.word, words.translation, lang_from, lang_to)

if __name__ == '__main__':
    # row(Het voertuig wordt verkocht in de staat als het zich bevindt, gekend door de koper na een testrit en, , [152, 1074, 828, 860])
    # row(uitgebreid onderzoek, rozległe badania, [144, 350, 862, 890])

    tmp:list[row] = [
        row([[152, 828], [1074, 828], [1074, 860], [152, 860]], "TEST 1", ""),
        row([[152, 828], [1074, 828], [1074, 860], [152, 860]], "TEST 2", ""),
        row([[152, 828], [1074, 828], [1074, 860], [152, 860]], "Het voertuig wordt verkocht in de staat als het zich bevindt, gekend door de koper na een testrit en", ""),
        row([[144, 862], [350, 862], [350, 890], [144, 890]], "uitgebreid onderzoek", "rozległe badania"),
        row([[152, 828], [1074, 828], [1074, 860], [152, 860]], "TEST 3", ""),
        row([[152, 828], [1074, 828], [1074, 860], [152, 860]], "TEST 4", "")
    ]

    # print(__create_full_sentences(tmp, "nl", debug=True))