import sys
import os

from program import program
from paths import save_logs

import tkinter as tk
from tkinter import filedialog, ttk

LEN_ARGS:int = 4

def open_menu():
    result = {"lang_from": "", "lang_to": ""}

    def on_ok():        
        result["lang_from"] = combo_from.get()
        result["lang_to"] = combo_to.get()
        root.quit()        

    def on_cancel():
        root.quit()

    root = tk.Tk()
    root.title("Wybór języków")

    tk.Label(root, text="Wybierz języki:").grid(row=0, column=0, columnspan=2, pady=5)

    tk.Label(root, text="Język źródłowy").grid(row=1, column=0, sticky="w", padx=5)
    combo_from = ttk.Combobox(root, values=["nl"])
    combo_from.set("nl")
    combo_from.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(root, text="Język docelowy").grid(row=2, column=0, sticky="w", padx=5)
    combo_to = ttk.Combobox(root, values=["pl"])
    combo_to.set("pl")
    combo_to.grid(row=2, column=1, padx=5, pady=5)

    btn_frame = tk.Frame(root)
    btn_frame.grid(row=3, column=0, columnspan=2, pady=10)

    tk.Button(btn_frame, text="OK", command=on_ok).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Anuluj", command=on_cancel).pack(side="left", padx=5)

    root.mainloop()

    root.destroy()
    return result["lang_from"], result["lang_to"]

def __check(cond:bool, msg:str, code:int=-1, debug:bool=False) -> None:
    if cond:
        save_logs(msg)

        if debug:
            print(msg)

        sys.exit(code)

def run(args:list[str], debug:bool=False) -> None:
    if debug:
        print("Załadowano ścieżki")

    __check(len(args) != LEN_ARGS, "Nieprawidłowa liczba argumentów wywołania programu", debug=debug)

    file_name:str = args[1]
    lang_from:str = args[2]
    lang_to:str = args[3]

    cur_dir:str = os.getcwd()
    full_path:str = os.path.join(cur_dir, file_name)

    __check(not os.path.exists(full_path), f"Plik >> {full_path} << nie istnieje", debug=debug)

    p = program(file_in=full_path, lang_from=lang_from, lang_to=lang_to, debug=debug)
    p.run()

if __name__ == '__main__':
    debug:bool = False   
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title="Wybierz plik",
        filetypes=[("Pliki graficzne", "*.jpg"), ("Pliki graficzne", "*.jpeg"), ("Pliki graficzne", "*.png")]
    )

    __check(file_path is None, "Nie wybrano pliku", debug=debug)
    root.quit()
    root.destroy()

    lang_from, lang_to = open_menu()
    print("Języki", lang_from, lang_to)

    __check(lang_from == "" or lang_to == "", "Nie wybrano języków", debug=debug)    

    run(['main.py', file_path, lang_from, lang_to], debug=debug)
