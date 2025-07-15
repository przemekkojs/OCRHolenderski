import sys
import os

from program import program

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Nieprawidłowa liczba argumentów wywołania programu")
        sys.exit(-1)

    file_name:str = sys.argv[1]
    cur_dir:str = os.getcwd()
    full_path:str = os.path.join(cur_dir, file_name)

    print("full_path:", full_path)

    if not os.path.exists(full_path):
        print("Plik nie istnieje")
        sys.exit(-1)

    p = program(file_in=full_path)
    p.exit()
