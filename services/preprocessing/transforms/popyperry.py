import cv2
import numpy as np


def bytes_to_np(img):
    np_arr = np.frombuffer(img, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    return img


def process_image(img):
    inverted = cv2.bitwise_not(img)
    return inverted


def np_to_png(img):
    success, encoded_img = cv2.imencode(".png", img)
    return encoded_img


def png_to_bytes(img):
    return img.tobytes()
