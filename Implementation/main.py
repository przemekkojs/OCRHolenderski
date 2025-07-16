import sys
import os

from program import program
from paths import save_logs, load_path

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
    p.run()

if __name__ == '__main__':
    run(['main.py', 'Implementation\\img\\test.jpg'], debug=True)
