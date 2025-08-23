from easyocr import Reader

from languages import check_if_language_exists
from ocr_models import ocr_models
from utils import draw_bounding_boxes
from complex_types import row

class ocr:
    def __init__(self, language:str, debug:bool=False):
        if not check_if_language_exists(language):
            raise ValueError(f"Language {language} is not supported")
        
        self.models = ocr_models(debug)
        self.debug:bool = debug
        self.reader:Reader = self.models[language]

    def __get_contents(self, file:str) -> list[dict[str, ] | str | list]:
        detail_level:int = 3 if self.debug else 1
        contents = self.reader.readtext(file, detail=detail_level, text_threshold=0.3, paragraph=False)

        if self.debug:
            draw_bounding_boxes(file, contents)

        return contents
        
    def read_full_list(self, file:str) -> list[dict[str, ] | str | list]:
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

    def read_points_and_words(self, file:str) -> list[row]:
        extracted = self.__get_contents(file)
        result:list[row] = []

        for item in extracted:
            result.append(row(
                coords=item[0],
                word=item[1].strip()
            ))
        
        return result
