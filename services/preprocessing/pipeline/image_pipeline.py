from pipeline.stages.background_removal import BackgroundRemovalStage
from pipeline.stages.grayscale import GrayscaleStage


class ImagePipeline:
    def __init__(self):
        self.bg_removal = BackgroundRemovalStage()
        self.grayscale = GrayscaleStage()

    def run(self, image):
        image = self.bg_removal.run(image)
        image = self.grayscale.run(image)

        return image
