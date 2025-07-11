from languages.languages import check_if_language_exists

def translate(what:str, lang_from:str, lang_to:str='pl') -> str:
    if not check_if_language_exists(lang_from):
        raise ValueError(f"Language {lang_from} is not supported")

    print(f"Translating phrase {what} from >> {lang_from} << to >> {lang_to} <<")
