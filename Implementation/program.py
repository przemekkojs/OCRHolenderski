import os

from ocr.ocr_reader import ocr
from standarizer.standarizer import process_image_file
from translator.translator import translate

from paths import *

class program:
    def __init__(self, file_in:str):
        self.file_in:str = file_in
    
