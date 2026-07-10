from typing import List

from db.meta_manager import MetaDatabaseManager
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse, Response
from schemas.models import Bow

router = APIRouter()

meta_manager = MetaDatabaseManager()


@router.post("/store")
async def store(bow: Bow = Depends(Bow.as_form), file: UploadFile = File(...)):
    try:
        # bow_data = Bow.parse_raw(bow)
        image_bytes = await file.read()

        meta_manager.store(bow, image_bytes)  # may raise ValueError
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    response = {"message": "success"}
    return JSONResponse(response)


@router.get("/image/{bow_id}")
def get_image(bow_id: str):
    try:
        result = meta_manager.search(bow_id)
        if not result or not result.get("images"):
            raise HTTPException(status_code=404, detail="Image not found")

        image_bytes = result["images"]
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    # assuming jpeg here; may want to detect or store the image MIME type
    return Response(content=image_bytes, media_type="image/jpeg")


@router.post("/search")
def search(bow_id: str):
    try:
        result = meta_manager.search(bow_id)
        if not result:
            raise HTTPException(status_code=404, detail="Bow not found")

        # remove since images are returned separately
        if "images" in result:
            result.pop("images")

        # parse result into Bow model
        bow_obj = Bow.parse_obj(result)

        # return serialised dict (Pydantic handles datetime serialization)
        # return JSONResponse(content=bow_obj.dict())
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    return bow_obj


@router.delete("/delete/{bow_id}")
def delete_bow(bow_id: str):
    try:
        meta_manager.delete(bow_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"bow_id": bow_id, "status": "deleted"}


@router.delete("/delete_all", status_code=status.HTTP_204_NO_CONTENT)
def delete_all_bows():
    try:
        meta_manager.delete_all()
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/list_all", response_model=List[Bow])
def list_all_bows():
    try:
        results = meta_manager.list_all()
        bows = [Bow.parse_obj(item) for item in results]

        if not bows:
            # return 404 if no valid bows found
            raise HTTPException(status_code=404, detail="No bows found")
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    return bows
