# Thanks to: https://medium.com/@nelsonizah/text-detection-in-images-with-easyocr-in-python-3e336c462c16
import cv2
import matplotlib.pyplot as plt

def draw_bounding_boxes(image, detections, threshold=0.25):
    img = cv2.imread(image)

    for (bbox, text, prob) in detections:
        (top_left, top_right, bottom_right, bottom_left) = bbox
        top_left = tuple(map(int, top_left))
        bottom_right = tuple(map(int, bottom_right))

        cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 2)
        cv2.putText(img, text, (top_left[0], top_left[1] - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.6, (0, 0, 255), 2)
    
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGBA))
    plt.axis('off')
    plt.show()
