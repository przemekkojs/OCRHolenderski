import os
import sys
import asyncio

from ocr_reader import ocr
from standarizer import process_image_file
from translator import translate
from paths import save_prefs, save_tmp, save_logs, save_any, load_path
from formatter import format_for_translation
from document import create_document
from languages import check_if_language_exists

class program:
    def __init__(self, file_in:str, debug:bool=False):
        self.file_in:str = file_in
        self.debug:bool = debug
        self.ocr:ocr = ocr('nl', debug)

        file_no_ext:str = os.path.basename(file_in).split('.')[0]
        file_succ_name:str = f"{file_no_ext}.docx"
        file_err_name:str = "niepowodzenie.txt"
        folder:str = os.path.dirname(file_in)
        
        self.folder:str = folder
        self.file_out_success:str = os.path.join(folder, file_succ_name)
        self.file_out_error:str = os.path.join(folder, file_err_name)

        self.contents:list[list[str | list]] = []

        self.result_success:bool = False
        self.log_contents:str = f"ROZPOCZĘCIE DZIAŁANIA PROGRAMU\nPLIK WEJŚCIOWY:\t{os.path.basename(file_in)}\nFOLDER:\t\t{folder}\nPLIK SUKCESU:\t{self.file_out_success}\nPLIK BŁEDU:\t{self.file_out_error}"
        
    def __extract_text(self) -> None:
        self.log_contents += "\n\nROZPOCZĘCIE EKSTRAKCJI TEKSTU"        

        try:
            base_name:str = os.path.basename(self.file_in)
            name_without_ext:str = os.path.splitext(base_name)[0]
            path_out:str = os.path.join(load_path("TMP_FOLDER"), f"{name_without_ext}.png")

            save_tmp(path_out, "")
            process_image_file(self.file_in, path_out, debug=self.debug)

            points_words:list[list[list | str]] = self.ocr.read_points_and_words(path_out)

            self.log_contents += "\nEKSTRAKCJA TEKSTU ZAKOŃCZONA POWODZENIEM"
            self.contents = format_for_translation(points_words)
        except Exception as e:
            details:str = str(e)
            self.log_contents += f"\n{details}"
            self.log_contents += "\nEKSTRAKCJA TEKSTU ZAKOŃCZONA NIEPOWODZENIEM"
            self.exit()

    # Tutaj trzeba zmienić NL i PL na parametry
    def __translate(self, lang_from:str, lang_to:str='pl') -> None:
        self.log_contents += "\n\nROZPOCZĘCIE TŁUMACZENIA TEKSTU"

        if not check_if_language_exists(lang_from):
            raise ValueError(f'Nieprawidłowy język źródłowy >> {lang_from} <<')
                
        try:
            asyncio.run(translate(self.contents, lang_from=lang_from, lang_to=lang_to))
            
            for row in self.contents:
                print(row[0], '=>', row[2])

            self.log_contents += "\nTŁUMACZENIE ZAKOŃCZONE POWODZENIEM"
        except Exception as e:
            details:str = str(e)
            self.log_contents += f"\n{details}"
            self.log_contents += "\nTŁUMACZENIE ZAKOŃCZONE NIEPOWODZENIEM"
            self.exit()

    def __create_document(self) -> None:
        self.log_contents += "\n\nROZPOCZĘCIE TWORZENIA DOKUMENTU"

        try:
            create_document(self.contents, self.file_out_success)

            self.log_contents += f"\nŚCIEŻKA DO DOKUMENTU: {self.file_out_success}"
            self.log_contents += "\nTWORZENIE DOKUMENTU ZAKOŃCZONE POWODZENIEM"
        except Exception as e:
            details:str = str(e)
            self.log_contents += f"\n{details}"
            self.log_contents += "\nTWORZENIE DOKUMENTU ZAKOŃCZONE NIEPOWODZENIEM"
            self.exit()

    # To trzeba jakoś fajnie zrobić
    def run(self, lang_from:str, lang_to:str='pl') -> None:
        self.__extract_text()
        self.__translate(lang_from, lang_to)
        self.__create_document()

        self.result_success = True
        self.exit()

    def exit(self) -> None:
        if self.result_success:
            self.log_contents += "\nDZIAŁANIE PROGRAMU ZAKONCZONE POWODZENIEM"
            file_to_save:str = self.file_out_success
        else:
            self.log_contents += f"\nPLIK BŁĘDU: {self.file_out_error}"
            self.log_contents += "\nDZIAŁANIE PROGRAMU ZAKONCZONE NIEPOWODZENIEM"
            file_to_save:str = self.file_out_error
            save_any(file_to_save, f"Program działał w {self.folder}\nPlik wejściowy: {self.file_in}")

        save_logs(self.log_contents)
        sys.exit(-1)
