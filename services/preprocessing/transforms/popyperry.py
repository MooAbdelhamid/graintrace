import cv2
import numpy as np


def image_process(img):
    np_arr = np.frombuffer(img, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    inverted = cv2.bitwise_not(img)
    success, encoded_img = cv2.imencode(".png", inverted)
    return encoded_img.tobytes()
