import torch
from pipeline.stages.inference_preprocessor import transform
from utils.model_loader import ModelLoader


class InferencePipeLine:
    def __init__(self, model_path, model_class, load_type, device=None):
        self.device = (
            device if device else ("cuda" if torch.cuda.is_available() else "cpu")
        )

        loader = ModelLoader(
            model_path=model_path,
            model_class=model_class,
            load_type=load_type,
            device=self.device,
        )

        self.model = loader.load().eval()

    def infer(self, image):
        image = transform(image)
        image = image.unsqueeze(0)
        with torch.no_grad():
            embeddings = self.model(image)
        return embeddings
