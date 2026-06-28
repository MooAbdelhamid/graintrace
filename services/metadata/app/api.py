from db.meta_manager import MetaDatabaseManager
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

meta_manager = MetaDatabaseManager()


@router.post("/store")
def store(bow_id: str, maker: str, bow_kind: str, owner: str):
    meta_manager.store(bow_id, maker, bow_kind, owner)
    response = {"message": "added success"}
    return JSONResponse(response)


@router.post("/search")
def search(bow_id: str):
    results = meta_manager.search(bow_id)
    bow_id, x, y, z, _ = results

    response = {"bow_id": bow_id, "x": x, "y": y, "z": z}

    return JSONResponse(response)
