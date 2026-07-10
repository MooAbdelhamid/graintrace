import numpy as np
from pipeline.stages.background_removal import BackgroundRemovalStage
from pipeline.stages.grayscale import GrayscaleStage
from pipeline.stages.object_crop import CropStage
from pipeline.stages.object_detection import ObjectDetectionStage


class ImagePipeline:
    """
    Input: Reconstructed Image
    """

    def __init__(self):
        self.detector = ObjectDetectionStage()
        self.cropper = CropStage()
        self.bg_removal = BackgroundRemovalStage()
        self.grayscale = GrayscaleStage()

    def run(self, image: np.ndarray) -> np.ndarray:
        result = self.detector.run(image)

        if result is None:
            return None

        image = self.bg_removal.run(image)

        image = self.cropper.run(image, result)

        if image is None:
            return None

        image = self.grayscale.run(image)

        return image

    def run_1(self, image: np.ndarray) -> np.ndarray:
        """
        old pipeline
        """
        image = self.bg_removal.run(image)

        image = self.grayscale.run(image)

        return image
