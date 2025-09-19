import json
import spacy

from spacy.cli import download
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

from paths import save_model, model_exists, model_path, filter_path
from languages import CODES_TO_MODEL_CODES, CODES_TO_FILTER_CODES

def __create_key(lang_from:str, lang_to:str) -> str:
    return f"{lang_from}_{lang_to}"

def __download_translation_model(lang_from:str, lang_to:str, debug:bool=False):
    key:str = __create_key(lang_from, lang_to)

    with open("models.json", 'r') as f:
        data = json.load(f)

    model_name:str = data[key]

    if model_name == "" or model_name is None:
        if debug:
            print(f"MODEL O NAZWIE {model_name} NIE ISTNIEJE W BAZIE")

        raise ValueError(f"Model for languages >> {key} << not found")

    if debug:
        print(f"POBIERANIE MODELU >> {model_name} <<")

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    if debug:
        print(f"POBIERANIE MODELU >> {model_name} << ZAKOŃCZONE")

    save_model(key, tokenizer, model)

    if debug:
        print(f"MODEL ZAPISANY POMYŚLNIE")

    return (tokenizer, model)

def get_filter_model(name:str, debug:bool=False):
    decoded_name:str = CODES_TO_FILTER_CODES[name]
    path:str = filter_path(decoded_name)
    model = spacy.load(path)

    return model

def get_translation_model(lang_from:str, lang_to:str, debug:bool=False):
    key:str = __create_key(lang_from, lang_to)

    if debug:
        print(f"UZYSKIWANIE DOSTĘPU DO MODELU >> {key} <<")

    exists:bool = model_exists(key)

    if exists:
        path:str = model_path(key)

        if debug:
            print(f"MODEL ISTNIEJE W >> {path} <<")

        tokenizer = AutoTokenizer.from_pretrained(path)
        model = AutoModelForSeq2SeqLM.from_pretrained(path)
    else:
        if debug:
            print("MODEL NIE ISTNIEJE LOKALNIE")

        tokenizer, model = __download_translation_model(lang_from, lang_to, debug)

    src_lang:str = CODES_TO_MODEL_CODES[lang_from]
    tgt_lang:str = CODES_TO_MODEL_CODES[lang_to]

    return pipeline("translation", model=model, tokenizer=tokenizer, src_lang=src_lang, tgt_lang=tgt_lang)

# DEVELOPMENT ONLY!
def __download_filter(name:str):
    path:str = filter_path(name)

    download(name)
    nlp = spacy.load(name)
    nlp.to_disk(path)
