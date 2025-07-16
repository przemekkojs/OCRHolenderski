from easyocr import Reader

from languages import SUPPORTED_LANGUAGES

class __ocr_models:
    def __init__(self):
        self.__models:dict[str, Reader] = {}

    def __getitem__(self, key:str) -> Reader:
        keys = self.__models.keys()

        if key in keys:
            return self.__models[key]
        else:
            print(f"Model for key \"{key}\" not found")
            return None
        
    def __setitem__(self, key:str, value:Reader) -> Reader:
        self.__models[key] = value


def __init_models(debug:bool=True):
    for language in SUPPORTED_LANGUAGES:
        ocr_models[language] = Reader([language], gpu=True)

        if debug:
            print(f"Zainicjowano model >> {language} <<")

ocr_models = __ocr_models()
__init_models()
