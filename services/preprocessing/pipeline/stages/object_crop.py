import numpy as np


class CropStage:
    def run(self, image: np.ndarray, result) -> np.ndarray | None:
        """
        Crops the first detected object and returns a square crop.

        Parameters
        ----------
        image : np.ndarray
            Original BGR image.

        result : ultralytics.engine.results.Results
            YOLO detection result.

        Returns
        -------
        np.ndarray or None
        """

        boxes = result.boxes.xyxy.cpu().numpy()

        if len(boxes) == 0:
            return None

        h_img, w_img = image.shape[:2]

        x1, y1, x2, y2 = boxes[0].astype(int)

        # Keep coordinates inside image
        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(w_img, x2)
        y2 = min(h_img, y2)

        box_w = x2 - x1
        box_h = y2 - y1

        if box_w <= 0 or box_h <= 0:
            return None

        square_size = max(box_w, box_h)

        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2

        new_x1 = cx - square_size // 2
        new_y1 = cy - square_size // 2
        new_x2 = new_x1 + square_size
        new_y2 = new_y1 + square_size

        # Shift crop if outside image
        if new_x1 < 0:
            new_x2 -= new_x1
            new_x1 = 0

        if new_y1 < 0:
            new_y2 -= new_y1
            new_y1 = 0

        if new_x2 > w_img:
            shift = new_x2 - w_img
            new_x1 -= shift
            new_x2 = w_img

        if new_y2 > h_img:
            shift = new_y2 - h_img
            new_y1 -= shift
            new_y2 = h_img

        new_x1 = max(0, new_x1)
        new_y1 = max(0, new_y1)
        new_x2 = min(w_img, new_x2)
        new_y2 = min(h_img, new_y2)

        return image[new_y1:new_y2, new_x1:new_x2]
