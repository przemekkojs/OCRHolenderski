import os

from ocr_reader import ocr
from standarizer import process_image_file
from translator import translate
from paths import save_prefs, save_tmp, save_logs, save_any

class program:
    def __init__(self, file_in:str, debug:bool=False):
        self.file_in:str = file_in
        self.debug:bool = debug
        self.ocr:ocr = ocr('nl')

        file_no_ext:str = os.path.basename(file_in).split('.')[0]
        file_succ_name:str = f"{file_no_ext}.docx"
        file_err_name:str = "niepowodzenie.txt"
        folder:str = os.path.dirname(file_in)
        
        self.folder:str = folder
        self.file_out_success:str = os.path.join(folder, file_succ_name)
        self.file_out_error:str = os.path.join(folder, file_err_name)

        self.result_success:bool = False
        self.log_contents:str = f"\
            ROZPOCZĘCIE DZIAŁANIA PROGRAMU\n\
            PLIK WEJŚCIOWY:\t{os.path.basename(file_in)}\n\
            FOLDER:\t\t{folder}\n\
            PLIK SUKCESU:\t{self.file_out_success}\n\
            PLIK BŁEDU:\t{self.file_out_error}"
        
    def __extract_text(self) -> None:
        self.log_contents += "\n\nROZPOCZĘCIE EKSTRAKCJI TEKSTU"
        self.log_contents += "\nEKSTRAKCJA TEKSTU ZAKOŃCZONA POWODZENIEM"

    def __translate(self) -> None:
        self.log_contents += "\n\nROZPOCZĘCIE TŁUMACZENIA TEKSTU"
        self.log_contents += "\nTŁUMACZENIE ZAKOŃCZONE POWODZENIEM"

    def __create_document(self) -> None:
        self.log_contents += "\n\nROZPOCZĘCIE TWORZENIA DOKUMENTU"
        self.log_contents += f"\nŚCIEŻKA DO DOKUMENTU: {'C:/Tu/Dać/Ściezkę'}"
        self.log_contents += "\nTWORZENIE DOKUMENTU ZAKOŃCZONE POWODZENIEM"

    # To trzeba jakoś fajnie zrobić
    def run(self) -> None:
        self.__extract_text()
        self.__translate()
        self.__create_document()

        self.result_success = True
        self.exit()

    def exit(self) -> None:
        if self.result_success:
            self.log_contents += "\nDZIAŁANIE PROGRAMU ZAKONCZONE POWODZENIEM"
            file_to_save:str = self.file_out_success
        else:
            self.log_contents += "\nDZIAŁANIE PROGRAMU ZAKONCZONE NIEPOWODZENIEM"
            file_to_save:str = self.file_out_error

        save_logs(self.log_contents)
        save_any(file_to_save, f"Program działał w {self.folder}\nPlik wejściowy: {self.file_in}")
