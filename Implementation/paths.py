from datetime import datetime
from docx import Document
from typing import overload

import os
import json

def load_path(key:str) -> None:
    with open("paths.json", "r", encoding="utf-8") as f:
        config = json.load(f)

    return os.path.normpath(config[key])

def __save(path:str, file_name:str, contents, debug:bool=False) -> None:
    full_path:str = os.path.join(path, file_name)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    _, extension = os.path.splitext(file_name)

    try:
        if extension == ".docx":
            doc = Document(full_path) if os.path.exists(full_path) else Document()
            doc.add_paragraph(contents)
            doc.save(full_path)
        else:        
            with open(full_path, 'w', encoding='utf-8') as file:
                file.write(contents)

        if debug:
            print(f"Zapisano >> {file_name} << do lokalizacji >> {full_path} <<")
    except Exception as e:
        save_logs(str(e))

        if debug:
            print(f"Zapisywanie >> {file_name} << do lokalizacji >> {full_path} << ZAKOŃCZONE NIEPOWODZENIEM")
            print(e)


@overload
def save_any(full_path: str, contents) -> None: ...
@overload
def save_any(path: str, file_name: str, contents) -> None: ...

def save_any(*args):
    if len(args) == 2:
        full_path, contents = args
        path:str = os.path.dirname(full_path)
        file_name:str = os.path.basename(full_path)
        __save(path, file_name, contents)
    elif len(args) == 3:
        path, file_name, contents = args        
        __save(path, file_name, contents)
    else:
        raise TypeError("save_any() expects 2 or 3 arguments")

def save_logs(contents) -> None:
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    __save(load_path("LOGS_FOLDER"), f"{now}.log", contents)

def save_tmp(file_name:str, contents) -> None:
    __save(load_path("TMP_FOLDER"), file_name, contents)

def save_prefs(file_name:str, contents) -> None:
    __save(load_path("PREFS_FOLDER"), file_name, contents)
