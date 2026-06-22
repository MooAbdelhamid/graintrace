import torch


class ModelLoader:
    def __init__(
        self, model_path, model_class=None, load_type="state_dict", device=None
    ):
        self.model_path = model_path
        self.model_class = model_class
        self.load_type = load_type
        self.device = (
            device if device else ("cuda" if torch.cuda.is_available() else "cpu")
        )

    def load(self):
        if self.load_type == "state_dict":
            model = self.model_class()
            checkpoint = torch.load(self.model_path, map_location=self.device)
            model.load_state_dict(checkpoint["model_state_dict"])

        elif self.load_type == "full_model":
            model = torch.load(self.model_path, map_location=self.device)

        else:
            raise ValueError("load_type must be 'state_dict' or 'full_model'")

        model.to(self.device)
        model.eval()
        return model
