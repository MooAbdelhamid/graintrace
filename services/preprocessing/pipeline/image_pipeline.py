import numpy as np
from pipeline.stages.background_removal import BackgroundRemovalStage
from pipeline.stages.grayscale import GrayscaleStage


class ImagePipeline:
    """
    Input: Reconstructed Image
    """

    def __init__(self):
        self.bg_removal = BackgroundRemovalStage()
        self.grayscale = GrayscaleStage()

    def run(self, image: np.ndarray) -> np.ndarray:

        image = self.bg_removal.run(image)

        image = self.grayscale.run(image)

        return image
