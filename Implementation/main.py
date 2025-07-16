import sys
import os

from program import program
from paths import save_logs

def __check(cond:bool, msg:str, code:int=-1, debug:bool=False) -> None:
    if cond:
        save_logs(msg)
        sys.exit(code)

def run(args:list[str], debug:bool=False) -> None:
    __check(len(args) != 2, "Nieprawidłowa liczba argumentów wywołania programu", debug=debug)

    file_name:str = args[1]
    cur_dir:str = os.getcwd()
    full_path:str = os.path.join(cur_dir, file_name)

    __check(not os.path.exists(full_path), "Plik nie istnieje", debug=debug)

    p = program(file_in=full_path)
    p.run()

if __name__ == '__main__':
    run(['main.py', 'img/test.jpg'])
