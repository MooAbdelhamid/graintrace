import cv2
import numpy as np


def decode_image(image_bytes: bytes) -> np.ndarray:
    """
    Converts from bytes to np
    """
    arr = np.frombuffer(image_bytes, np.uint8)  # array of bytes

    image = cv2.imdecode(arr, cv2.IMREAD_COLOR)  # reconstructed image

    return image


def encode_image(image: np.ndarray, ext=".png") -> bytes:
    """
    Converts from np to bytes
    """
    _, buf = cv2.imencode(ext, image)

    return buf.tobytes()
