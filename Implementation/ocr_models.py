from easyocr import Reader
import os

from languages import SUPPORTED_LANGUAGES
from paths import load_path

class ocr_models:
    def __init__(self, debug:bool=False):
        self.debug:bool = debug
        self.__models:dict[str, Reader] = {}
        
        for language in SUPPORTED_LANGUAGES:
            self.__models[language] = Reader([language], gpu=True)

            if debug:
                print(f"Zainicjowano model >> {language} <<")

            language_path:str = os.path.join(load_path("DICT_FOLDER"), f"{language}.json")
            
            if not os.path.exists(language_path):
                path:str = os.path.dirname(language_path)
                os.mkdir(path)

                with open(language_path, 'w', encoding='utf-8') as file:
                    pass

                if debug:
                    print(f'Utworzono plik słownika >> {language_path} <<')
            elif debug:
                print(f'Plik słownika >> {language_path} << już istnieje')

    def __getitem__(self, key:str) -> Reader:
        keys = self.__models.keys()

        if key in keys:
            return self.__models[key]
        else:
            if self.debug:
                print(f"Model for key \"{key}\" not found")

            return None
        
    def __setitem__(self, key:str, value:Reader) -> Reader:
        self.__models[key] = value

