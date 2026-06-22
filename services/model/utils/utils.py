import cv2
import numpy as np
from PIL import Image


def decode_image(image_bytes: bytes) -> np.ndarray:
    """
    Converts from bytes to image
    """
    # bytes -> numpy array
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)

    # decode with OpenCV (BGR)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    # BGR -> RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # numpy -> PIL
    image = Image.fromarray(image)

    return image


def encode_image(image: np.ndarray, ext=".png") -> bytes:
    """
    Converts from tensor to bytes
    """
    pass
