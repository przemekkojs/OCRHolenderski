from languages import check_if_language_exists

# Wsm to zaimplementować i reszta działa
def translate_word(what:str, lang_from:str, lang_to:str='pl') -> str:
    if what == "":
        return ""

    if not check_if_language_exists(lang_from):
        raise ValueError(f"Language {lang_from} is not supported")

    print(f"Tłumaczenie {what} z >> {lang_from} << na >> {lang_to} <<")
    return "TODO"

def translate(input: dict[str, list[list, str]], lang_from:str, lang_to:str='pl') -> None:
    keys = input.keys()

    for key in keys:
        tpl:tuple[list, str] = input[key]
        word:str = tpl[1]
        translated_word:str = translate_word(word, lang_from, lang_to)
        translated_word = "NIEPOWODZENIE" if translated_word == "" else translated_word
        input[key][1] = translated_word

def translate_word_list(input: list[str], lang_from:str, lang_to:str='pl') -> list[str]:
    result:list[str] = []

    for word in input:
        translated_word:str = translate_word(word, lang_from, lang_to)
        result.append(translated_word)

    return result
