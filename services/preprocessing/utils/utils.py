import cv2
import numpy as np


def decode_image(image_bytes: bytes) -> np.ndarray:
    arr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    return image


def encode_image(image: np.ndarray, ext=".png") -> bytes:
    _, buf = cv2.imencode(ext, image)
    return buf.tobytes()
