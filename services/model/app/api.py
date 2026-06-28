from fastapi import APIRouter, File, UploadFile
from pipeline.inferencepipeline import InferencePipeLine
from pipeline.models_architectures import ConResNet50
from utils.utils import decode_image

router = APIRouter()

model_path = ".\pipeline\model_weights\GrainTrace_Experiment_Hard_Weights.pth"
inference_pipeline = InferencePipeLine(model_path, ConResNet50, "state_dict")


@router.post("/infer")
async def pipeline(file: UploadFile = File(...)):

    content = await file.read()

    image = decode_image(content)

    embeddings = inference_pipeline.infer(image)  # Tensor

    embeddings = embeddings.cpu().squeeze().numpy().tolist()

    return {"embeddings": embeddings}
