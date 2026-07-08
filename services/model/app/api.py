from fastapi import APIRouter, File, UploadFile
from pipeline.inferencepipeline import InferencePipeLine
from pipeline.models_architectures import ConResNet50, DINOv2EmbeddingModel
from utils.utils import decode_image

router = APIRouter()

model_path_res = ".\pipeline\model_weights\Resnet_Final.pth"
model_path_dino = ".\pipeline\model_weights\Dino_Final.pth"

inference_pipeline_res = InferencePipeLine(model_path_res, ConResNet50, "state_dict")
inference_pipeline_dino = InferencePipeLine(
    model_path_dino, DINOv2EmbeddingModel, "state_dict"
)


@router.post("/infer")
async def pipeline(file: UploadFile = File(...)):

    content = await file.read()

    image = decode_image(content)

    embeddings = inference_pipeline_dino.infer(image)  # Tensor

    embeddings = embeddings.cpu().squeeze().numpy().tolist()

    return {"embeddings": embeddings}
