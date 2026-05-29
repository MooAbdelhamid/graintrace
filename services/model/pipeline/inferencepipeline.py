import torch
from utils.model_loader import ModelLoader

loader = ModelLoader()


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

        self.model = loader.load()
