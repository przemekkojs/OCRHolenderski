from ocr_reader import ocr
from Implementation.standarizer import process_image_file
from logger import log
from paths import *

import os

__test_files_dir:str = "TestImages/src"
__out_files_dir:str = "TestImages/out"
OCR = ocr('nl')

def __stats(result:list, debug:bool=False) -> float:
    sum:float = 0
    cnt:int = 0

    for item in result:
        sum += item[2]
        cnt += 1

    acc:float = sum / cnt

    if debug:
        print("acc", acc)
        print("sum", sum)
        print("cnt", cnt)

    return acc

def __test_one_file(debug:bool=False) -> None:
    process_image_file(
        image_path=f"{__test_files_dir}/20250601_133903.jpg",
        output_path=f"{__out_files_dir}/20250601_133903.png",
        debug=debug)
    
    result = OCR.read_full_list(f"{__out_files_dir}/20250601_133903.png")                        
    __stats(result, debug)

def __test_all(debug:bool=False) -> None:
    count:int = 0
    sum:float = 0

    for filename in os.listdir(__test_files_dir):
        png_filename = f"{filename.split('.')[0]}.png"

        path_raw = f"{__test_files_dir}/{filename}"
        path_processed = f"{__out_files_dir}/{png_filename}"

        try:
            process_image_file(
                image_path=path_raw,
                output_path=path_processed,
                debug=debug)

            result = OCR.read_full_list(path_processed)                  
            sum += __stats(result, debug)            
        except Exception as e:
            print(f"Nie udało się przetworzyć obrazu \"{png_filename}\"")
            print(e)

        count += 1

    avg_acc:float = sum / count

    print("ŚREDNIA DOKŁADNOŚĆ ZE WSZYSTKICH:", avg_acc)

def __test_text(debug:bool=False) -> None:
    process_image_file(
        image_path=f"{__test_files_dir}/20250601_133903.jpg",
        output_path=f"{__out_files_dir}/20250601_133903.png",
        debug=debug)
    
    result = OCR.read_text_only(f"{__out_files_dir}/20250601_133903.png")
    print(result)

def __info_simple() -> None:
    log("This is some info")

def __warning_simple() -> None:
    log("This is some warning", level=1)

def __error_simple() -> None:
    log("This is some error", level=2)

def __create_files_in_paths() -> None:
    file_name:str = "test.txt"
    tmp_path:str = f"{load_path('TMP_FOLDER')}/{file_name}"
    prefs_path:str = f"{load_path('PREFS_FOLDER')}/{file_name}"

    message:str = "Szybki test, czy zapisywanie działa"

    os.makedirs(os.path.dirname(tmp_path), exist_ok=True)
    os.makedirs(os.path.dirname(prefs_path), exist_ok=True)

    with open(tmp_path, 'w', encoding='utf-8') as file:
        file.write(message)

    with open(prefs_path, 'w', encoding='utf-8') as file:
        file.write(message)

def __log_error_to_file() -> None:
    log("Jakiś błąd", 2, save_logs)

if __name__ == '__main__':
    # __test_one_file()
    # __test_all()
    # __test_text()

    # __info_simple()
    # __warning_simple()
    # __error_simple()

    #__create_files_in_paths()
    #__log_error_to_file()

    pass