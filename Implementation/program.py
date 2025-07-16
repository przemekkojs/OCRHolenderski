import os

from ocr_reader import ocr
from Implementation.standarizer import process_image_file
from Implementation.translator import translate
from paths import save_prefs, save_tmp, save_logs, save_any

class program:
    def __init__(self, file_in:str):
        self.file_in:str = file_in

        file_no_ext:str = os.path.basename(file_in).split('.')[0]
        file_succ_name:str = f"{file_no_ext}.docx"
        file_err_name:str = "niepowodzenie.txt"
        folder:str = os.path.dirname(file_in)
        
        self.folder:str = folder
        self.file_out_success:str = os.path.join(folder, file_succ_name)
        self.file_out_error:str = os.path.join(folder, file_err_name)

        self.result_success:bool = True
        self.log_contents:str = f"\
            ROZPOCZĘCIE DZIAŁANIA PROGRAMU\n\
            PLIK WEJŚCIOWY:\t{os.path.basename(file_in)}\n\
            FOLDER:\t\t{folder}\n\
            PLIK SUKCESU:\t{self.file_out_success}\n\
            PLIK BŁEDU:\t{self.file_out_error}"

    def exit(self) -> None:
        if self.result_success:
            self.log_contents += "\nDZIAŁANIE PROGRAMU ZAKONCZONE POWODZENIEM"
            file_to_save:str = self.file_out_success
        else:
            self.log_contents += "\nDZIAŁANIE PROGRAMU ZAKONCZONE NIEPOWODZENIEM"
            file_to_save:str = self.file_out_error

        save_logs(self.log_contents)
        save_any(file_to_save, f"Program działał w {self.folder}\nPlik wejściowy: {self.file_in}")
