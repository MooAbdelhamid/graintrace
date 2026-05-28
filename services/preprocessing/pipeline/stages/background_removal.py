import cv2
import numpy as np
from transparent_background import Remover


class BackgroundRemovalStage:
    def __init__(self, mode: str = "base"):
        self.remover = Remover(mode=mode)

    def run(self, image: np.ndarray) -> np.ndarray:
        """
        image: BGR image (OpenCV format)
        returns: BGR image with background removed (masked)
        """

        # Convert BGR -> RGB ONLY for model compatibility
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Run model
        out = self.remover.process(rgb, type="rgba")

        rgba = np.array(out)
        alpha = rgba[:, :, 3]

        # Apply alpha mask on original BGR image
        masked = cv2.bitwise_and(image, image, mask=alpha)

        return masked
