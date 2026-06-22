import torch
from torchvision import transforms
from utils.model_loader import ModelLoader

transform_resize = transforms.Resize((224 * 4, 224 * 4))
transform_normalize = transforms.Normalize(
    mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
)

transform_1 = transforms.Compose(
    [transform_resize, transforms.ToTensor(), transform_normalize]
)


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
        image = transform_1(image)
        image = image.unsqueeze(0)
        with torch.no_grad():
            embeddings = self.model(image)
        return embeddings
