import sys
import os

from program import program
from paths import save_logs

import tkinter as tk
from tkinter import filedialog

def __check(cond:bool, msg:str, code:int=-1, debug:bool=False) -> None:
    if cond:
        save_logs(msg)

        if debug:
            print(msg)

        sys.exit(code)

def run(args:list[str], debug:bool=False) -> None:
    if debug:
        print("Załadowano ścieżki")

    __check(len(args) != 2, "Nieprawidłowa liczba argumentów wywołania programu", debug=debug)

    file_name:str = args[1]
    cur_dir:str = os.getcwd()
    full_path:str = os.path.join(cur_dir, file_name)

    __check(not os.path.exists(full_path), f"Plik >> {full_path} << nie istnieje", debug=debug)

    p = program(file_in=full_path, debug=debug)
    p.run(lang_from='nl', lang_to='pl')

if __name__ == '__main__':
    debug:bool = False
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title="Wybierz plik",
        filetypes=[("Pliki graficzne", "*.jpg"), ("Pliki graficzne", "*.jpeg"), ("Pliki graficzne", "*.png")]
    )

    __check(file_path is None, "Nie wybrano pliku", debug=debug)
    run(['main.py', file_path], debug=debug)
