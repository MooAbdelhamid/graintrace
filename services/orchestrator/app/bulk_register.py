import json
import uuid

import pandas as pd
from clients.metadata import meta_store
from clients.model import model_call
from clients.preprocessing import preprocessing_call
from clients.retrieval import retrieval_store
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from models.bow import Bow

router = APIRouter(prefix="/bulk_register", tags=["bulk_register"])


def generate_bow_id() -> str:
    # orchestrator assigns bow_id in format BOW-XXXXXX
    return f"BOW-{uuid.uuid4().hex[:6].upper()}"


def clean_value(value):
    if pd.isna(value):
        return None
    return value


def row_to_bow(row) -> Bow:

    materials = None

    if clean_value(row.get("materials")):
        materials = json.loads(row["materials"])

    return Bow(
        maker=clean_value(row["maker"]),
        bow_kind=clean_value(row.get("bow_kind")),
        brand=clean_value(row.get("brand")),
        school=clean_value(row.get("school")),
        owner=clean_value(row.get("owner")),
        maker_assigned_id=clean_value(row.get("maker_assigned_id")),
        certificate_no=clean_value(row.get("certificate_no")),
        stick_id_no=clean_value(row.get("stick_id_no")),
        proof_created_by=clean_value(row.get("proof_created_by")),
        place_of_issue=clean_value(row.get("place_of_issue")),
        date_of_issue=clean_value(row.get("date_of_issue")),
        wood_registration_date=clean_value(row.get("wood_registration_date")),
        import_proof=clean_value(row.get("import_proof")),
        materials=materials,
        notes=clean_value(row.get("notes")),
    )


@router.post("/")
async def bulk_register(csv: UploadFile = File(...)):

    print("Bulk request received")

    df = pd.read_csv(csv.file)

    print(df)

    results = []

    for index, row in df.iterrows():
        try:
            print(f"Processing row {index}")

            print("ID Generated")
            bow_id = generate_bow_id()
            bow = row_to_bow(row)
            bow.id = bow_id

            # Load image

            image_path = row["image_path"]

            with open(image_path, "rb") as f:
                content = f.read()

            data = {"filename": image_path.split("/")[-1], "type": "image/jpeg"}

            # Preprocessing
            print("Calling Preprocessing")
            img = preprocessing_call(content, data)

            if img == b"null":
                results.append(
                    {"bow_id": bow_id, "status": "failed", "reason": "invalid image"}
                )
                continue

            # Embedding
            print("Calling Model")
            embedding_bytes = model_call(img, data)

            embeddings = json.loads(embedding_bytes.decode("utf-8"))

            embeddings = embeddings["embeddings"]

            # Retrieval
            print("Calling Retrieval")
            retrieval_result = retrieval_store(bow_id, embeddings)

            if retrieval_result["status"] == "duplicate":
                results.append({"bow_id": bow_id, "status": "duplicate"})
                continue

            # Metadata
            print("Calling Metadata")
            metadata_result = meta_store(bow, content)

            results.append({"bow_id": bow_id, "status": "success"})

        except Exception as e:
            results.append({"row": index, "status": "failed", "error": str(e)})

    return JSONResponse({"total": len(df), "results": results})
