from datetime import datetime
import os

TMP_FOLDER:str = "C:/Users/Public/Documents/Translator/tmp"
PREFS_FOLDER:str = "C:/Users/Public/Documents/Translator/prefs"
LOGS_FOLDER:str = "C:/Users/Public/Documents/Translator/logs"

def __save(path:str, file_name:str, contents, debug:bool=False) -> None:
    full_path:str = f"{path}/{file_name}"

    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    try:
        with open(full_path, 'w', encoding='utf-8') as file:
            file.write(contents)

        if debug:
            print(f"Zapisano >> {file_name} << do lokalizacji >> {full_path} <<")
    except Exception as e:
        if debug:
            print(f"Zapisywanie >> {file_name} << do lokalizacji >> {full_path} << ZAKOŃCZONE NIEPOWODZENIEM")

def save_logs(contents) -> None:
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    __save(LOGS_FOLDER, f"{now}.log", contents)

def save_tmp(file_name:str, contents) -> None:
    __save(TMP_FOLDER, file_name, contents)

def save_prefs(file_name:str, contents) -> None:
    __save(PREFS_FOLDER, file_name, contents)
