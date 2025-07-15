import os

from ocr.ocr_reader import ocr
from standarizer.standarizer import process_image_file
from translator.translator import translate

from paths import save_prefs, save_tmp

class program:
    def __init__(self, file_in:str):
        self.file_in:str = file_in

        file_no_ext:str = file_in.split('.')[0]
        folder:str = os.path.dirname(file_in)
        
        self.folder:str = folder
        self.file_out_success:str = f"{folder}/{file_no_ext}.docx"
        self.file_out_error:str = f"{folder}/niepowodzenie.txt"

