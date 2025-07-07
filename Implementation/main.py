from ocr.ocr_learning import ocr
from standarizer.standarizer import test

def __test():
    file = "Implementation/ocr/scanned.png"
    test("Implementation/ocr/file.jpeg", file)

    OCR = ocr('nl')
    result = OCR.read(file)

    acc:float = 0
    cnt:int = 0

    for item in result:
        acc += item[2]
        cnt += 1

    print(acc / cnt)
    print("acc", acc)
    print("cnt", cnt)


if __name__ == '__main__':
    __test()
