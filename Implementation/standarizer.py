import cv2
import numpy as np

def __binary_threshold_rgb(image):
    color_val:int = 123
    threshold:np.ndarray = np.array([color_val, color_val, color_val])
    mask = np.all(image > threshold, axis=2)

    result = np.zeros_like(image)
    result[mask] = [255, 255, 255]

    return result

def __order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")

    s = pts.sum(axis=1)
    diff = np.diff(pts, axis=1)

    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect

def __add_border_lines(image) -> None:
    line_width = 15
    black = (0, 0, 0)
    x = image.shape[0] - 1
    y = image.shape[1]

    cv2.line(image, (0, 0), (y, 0), black, line_width) # G
    cv2.line(image, (0, x), (y, x), black, line_width) # D    
    cv2.line(image, (0, 0), (0, x), black, line_width) # L
    cv2.line(image, (y, 0), (y, x), black, line_width) # P

def __window(name:str, size:tuple[int, int], file) -> None:
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(name, size[0], size[1])
    cv2.imshow(name, file) 

def process_image_file(image_path:str, output_path:str, output_size:tuple[int, int]=(1240, 1754), debug:bool=False, show_images:bool=False):
    image = cv2.imread(image_path)
    orig = image.copy()
    
    if debug and show_images:
        __window("Orig", (1240, 1754), orig)
        cv2.waitKey(0)

    __add_border_lines(image)    
    image = __binary_threshold_rgb(image)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    contours, _ = cv2.findContours(gray, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    if debug and show_images:
        __window("Image", (1240, 1754), image)
        cv2.waitKey(0)
        __window("Gray", (1240, 1754), gray)
        cv2.waitKey(0)

    document_contour = None

    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        
        if len(approx) == 4:
            document_contour = approx
            break
    
    if debug:
        if document_contour is not None:
            if show_images:    
                cv2.drawContours(orig, [document_contour], -1, (0, 255, 0), 3)
                __window("Contours", (1240, 1754), orig)
                cv2.waitKey(0)
        else:
            print("Nie znaleziono konturu o 4 narożnikach.")

    pts = document_contour.reshape(4, 2)
    rect = __order_points(pts)

    (tl, tr, br, bl) = rect

    widthA = np.linalg.norm(br - bl)
    widthB = np.linalg.norm(tr - tl)
    maxWidth = int(max(widthA, widthB))

    heightA = np.linalg.norm(tr - br)
    heightB = np.linalg.norm(tl - bl)
    maxHeight = int(max(heightA, heightB))

    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]
    ], dtype="float32")

    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(orig, M, (maxWidth, maxHeight))

    sharpen_kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    sharpened = cv2.filter2D(warped, -1, sharpen_kernel)
    enhanced = cv2.convertScaleAbs(sharpened, alpha=1.3, beta=15)
    standardized = cv2.resize(src=enhanced, dsize=output_size, interpolation=cv2.INTER_CUBIC)
    cv2.imwrite(output_path, standardized)

    if debug:
        if show_images:
            __window("Standardized", (1240, 1754), standardized)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            
        print(f"Zapisano plik: >> {output_path} <<")
    
