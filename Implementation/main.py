from ocr.ocr_learning import ocr
from standarizer.standarizer import process_image_file

def __stats(result):
    acc:float = 0
    cnt:int = 0

    for item in result:
        acc += item[2]
        cnt += 1

    print(acc / cnt)
    print("acc", acc)
    print("cnt", cnt)

def __test():
    file = "TestImages/out/scanned.png"
    process_image_file("TestImages/src/file.jpeg", file)

    OCR = ocr('nl')
    result = OCR.read(file)

    __stats(result)

if __name__ == '__main__':
    __test()
