import asyncio

from languages import check_if_language_exists
from paths import get_phrase_from_dictionary, set_phrase_to_dictionary
from complex_types import row, buffer_row
from translator_models import get_translation_model, get_filter_model

async def __translate_word_model(what:str, dictionary:dict[str, str], lang_from:str, _translator, _nlp, buffer:list[buffer_row], lang_to:str='pl', debug:bool=False) -> str:
    if debug:
        print(f"Tłumaczenie {what} z >> {lang_from} << na >> {lang_to} << z użyciem modelu")

    if not check_if_language_exists(lang_from):
        raise ValueError(f"Language {lang_from} is not supported")    

    if what == "":
        return ""
    
    if _translator is None:
        if debug:
            print("Obiekt >> _translator << nie został zdefiniowany")
        
        return ""
    
    if _nlp is None:
        if debug:
            print("Obiekt >> _nlp << nie został zdefiniowany")
        
        return ""
    
    loop = asyncio.get_running_loop()
    dictionary_translation: str = await get_phrase_from_dictionary(what, dictionary, debug)

    if dictionary_translation != "":
        if debug:
            print("Tłumaczenie znalezione w słowniku")
        return dictionary_translation

    if debug:
        print("Tłumaczenie z użyciem modelu")

    doc = _nlp(what)
    entities = {}
    protected_text = what

    if debug:
        print("ENCJE:")

    allowed_labels:set[str] = {"PERSON", "LOC", "FAC", "GPE", "ADDRESS"}

    for i, ent in enumerate(doc.ents):
        if ent.label_ not in allowed_labels:
            continue

        if debug:
            print(ent)

        placeholder = f"<ENT{i}>"
        entities[placeholder] = ent.text
        protected_text = protected_text.replace(ent.text, placeholder)

    if debug:
        print()

    result = await loop.run_in_executor(None, lambda: _translator(protected_text)[0]["translation_text"])   

    for placeholder, original in entities.items():
        result = result.replace(placeholder, original)

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

async def translate(input: list[row], dictionary:dict[str, str], lang_from:str, lang_to:str='pl', debug:bool=False) -> None:
    __translation_buffer:list[buffer_row] = []
    _translator = get_translation_model(lang_from, lang_to, debug)
    _nlp = get_filter_model(lang_from, debug)

    tasks:list = []    
    sentences:list[row] = __create_full_sentences(input, lang_from, debug=debug)

    for current_row in sentences:
        word:str = current_row.word        
        tasks.append(__translate_word_model(word, dictionary, lang_from, _translator, _nlp, buffer=__translation_buffer, lang_to=lang_to, debug=debug))

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
        await set_phrase_to_dictionary(words.word, words.translation, dictionary, lang_from, lang_to, debug)
