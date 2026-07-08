from ultralytics import YOLO

MODEL_PATH = r".\utils\my_model.pt"


class ObjectDetectionStage:
    def __init__(self, conf_threshold: float = 0.25):
        self.model = YOLO(MODEL_PATH)
        self.conf_threshold = conf_threshold

    def run(self, image):
        """
        Parameters
        ----------
        image : np.ndarray
            BGR OpenCV image.

        Returns
        -------
        Results
            Ultralytics Results object, or None if nothing detected.
        """

        results = self.model.predict(
            source=image, conf=self.conf_threshold, verbose=False
        )

        result = results[0]

        if result.boxes is None or len(result.boxes) == 0:
            print("Object not detected")
            return None

        return result
