from easyocr import Reader

from languages.languages import check_if_language_exists
from ocr.ocr_models import ocr_models

class ocr:
    def __init__(self, language:str):
        if not check_if_language_exists(language):
            raise ValueError(f"Language {language} is not supported")

        self.reader:Reader = ocr_models[language]

    def __get_contents(self, file:str) -> list:
        return self.reader.readtext(file)
        
    def read_full_list(self, file:str) -> list:
        return self.__get_contents(file)
    
    def read_text_only(self, file:str) -> str:
        extracted = self.__get_contents(file)
        text:str = ""

        for item in extracted:
            word:str = item[1].strip()
            text += f"{word} "
        
        text = text.strip()
        return text
    
    def read_words_list(self, file:str) -> list[str]:
        extracted = self.__get_contents(file)
        result:list[str] = []

        for item in extracted:
            word:str = item[1].strip()
            result.append(word)
        
        return result

    def read_points_and_words(self, file:str) -> list[tuple[list, str]]:
        extracted = self.__get_contents(file)
        result:list[list, str] = []

        for item in extracted:
            points:list = item[0]
            word:str = item[1].strip()
            result.append((points, word))
        
        return result

