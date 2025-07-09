from ocr.ocr_learning import ocr
from standarizer.standarizer import process_image_file

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
    
    result = OCR.read(f"{__out_files_dir}/20250601_133903.png")                        
    __stats(result, debug)

def __test_all(debug:bool=False):
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

            result = OCR.read(path_processed)                  
            sum += __stats(result, debug)            
        except Exception as e:
            print(f"Nie udało się przetworzyć obrazu \"{png_filename}\"")
            print(e)

        count += 1

    avg_acc:float = sum / count

    print("ŚREDNIA DOKŁADNOŚĆ ZE WSZYSTKICH:", avg_acc)

if __name__ == '__main__':
    # __test_one_file()
    __test_all()
