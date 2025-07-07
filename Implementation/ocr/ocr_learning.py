from easyocr import Reader

from languages.languages import check_if_language_exists
from ocr.ocr_models import ocr_models

class ocr:
    def __init__(self, language:str):
        if not check_if_language_exists(language):
            raise ValueError(f"Language {language} is not supported")

        self.reader:Reader = ocr_models[language]

    def read(self, file:str) -> list:
        return self.reader.readtext(file)
    
