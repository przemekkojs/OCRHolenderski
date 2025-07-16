import sys
import os

from program import program
from paths import save_logs

def __check(cond:bool, msg:str, code:int=-1) -> None:
    if cond:
        save_logs(msg)
        sys.exit(code)

def run(args:list[str], debug:bool=False) -> None:
    __check(len(args) != 2, "Nieprawidłowa liczba argumentów wywołania programu")

    file_name:str = args[1]
    cur_dir:str = os.getcwd()
    full_path:str = os.path.join(cur_dir, file_name)

    __check(not os.path.exists(full_path), "Plik nie istnieje")

    p = program(file_in=full_path)
    p.exit()

if __name__ == '__main__':
    run(sys.argv)
