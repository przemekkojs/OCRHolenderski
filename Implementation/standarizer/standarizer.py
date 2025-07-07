import cv2
import numpy as np

def binary_threshold_rgb(image):
    threshold = np.array([123, 123, 123])
    mask = np.all(image > threshold, axis=2)

    result = np.zeros_like(image)
    result[mask] = [255, 255, 255]

    return result

def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")

    s = pts.sum(axis=1)
    diff = np.diff(pts, axis=1)

    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect

def test(image_path:str, output_path:str, debug:bool=False):
    image = cv2.imread(image_path)
    line_width = 15
    cv2.line(image, (0, 0), (image.shape[1], 0), (0, 0, 0), line_width) # G
    cv2.line(image, (0, image.shape[0] - 1), (image.shape[1], image.shape[0] - 1), (0, 0, 0), line_width) # D    
    cv2.line(image, (0, 0), (0, image.shape[0] - 1), (0, 0, 0), line_width) # L
    cv2.line(image, (image.shape[1], 0), (image.shape[1], image.shape[0] - 1), (0, 0, 0), line_width) # P

    orig = image.copy()
    image = binary_threshold_rgb(image)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)    
    edges = cv2.Canny(gray, threshold1=150, threshold2=200)
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    
    document_contour = None

    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        
        if len(approx) == 4:
            document_contour = approx
            break
    
    if debug:
        if document_contour is not None:            
                cv2.drawContours(orig, [document_contour], -1, (0, 255, 0), 3)
                cv2.imshow("Znaleziony kontur dokumentu", orig)
                cv2.waitKey(0)
        else:
            print("Nie znaleziono konturu o 4 narożnikach.")

    pts = document_contour.reshape(4, 2)
    rect = order_points(pts)

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

    if debug:
        cv2.imshow("Wyostrzony skan", enhanced)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    cv2.imwrite(output_path, enhanced)   
    
