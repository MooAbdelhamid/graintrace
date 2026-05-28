import cv2
import numpy as np
from transparent_background import Remover


class ImagePreprocessingPipeline:
    def __init__(self, mode: str = "base"):
        self.remover = Remover(mode=mode)

    def run(self, img):
        # background removal
        out = self.remover.process(img, type="rgba")

        # alpha mask
        rgba = np.array(out)
        alpha = rgba[:, :, 3]

        # apply mask
        segmented = cv2.bitwise_and(img, img, mask=alpha)

        # grayscale
        gray = cv2.cvtColor(segmented, cv2.COLOR_BGR2GRAY)

        return gray

    def run_1(self, img):
        # step 1: bg removal -> rgba
        # img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        out = self.remover.process(img, type="rgba")

        # step 2: black background via alpha mask on original
        rgba = np.array(out)
        alpha = rgba[:, :, 3]  # mask
        roi = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)  # rgb -> bgr
        segmented = cv2.bitwise_and(roi, roi, mask=alpha)

        # step 3: grayscale
        gray = cv2.cvtColor(segmented, cv2.COLOR_BGR2GRAY)

        # _, buf = cv2.imencode(".png", gray)
        return gray
