import cv2
import numpy as np


def decode_image(image_bytes: bytes) -> np.ndarray:
    """
    Converts from bytes to nparray
    """
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)

    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    return image


def encode_image(image: np.ndarray, ext=".png") -> bytes:
    """
    Converts from tensor to bytes
    """
    pass
