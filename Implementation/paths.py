from datetime import datetime
import os
from typing import overload

TMP_FOLDER:str = "C:/Users/Public/Documents/Translator/tmp"
PREFS_FOLDER:str = "C:/Users/Public/Documents/Translator/prefs"
LOGS_FOLDER:str = "C:/Users/Public/Documents/Translator/logs"

def __save(path:str, file_name:str, contents, debug:bool=False) -> None:
    full_path:str = os.path.join(path, file_name)

    print(full_path)

    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    try:
        with open(full_path, 'w', encoding='utf-8') as file:
            file.write(contents)

        if debug:
            print(f"Zapisano >> {file_name} << do lokalizacji >> {full_path} <<")
    except Exception as e:
        if debug:
            print(f"Zapisywanie >> {file_name} << do lokalizacji >> {full_path} << ZAKOŃCZONE NIEPOWODZENIEM")


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
    __save(LOGS_FOLDER, f"{now}.log", contents)

def save_tmp(file_name:str, contents) -> None:
    __save(TMP_FOLDER, file_name, contents)

def save_prefs(file_name:str, contents) -> None:
    __save(PREFS_FOLDER, file_name, contents)
