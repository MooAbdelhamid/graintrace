from db.meta_manager import MetaDatabaseManager
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

meta_manager = MetaDatabaseManager()


@router.post("/store")
def store(bow_id: str, maker: str, bow_kind: str, owner: str):
    meta_manager.store(bow_id, maker, bow_kind, owner)
    response = {"message": "success"}
    return JSONResponse(response)


@router.post("/search")
def search(bow_id: str):
    results = meta_manager.search(bow_id)
    if results:
        bow_id, maker, bow_kind, owner, _ = results
        response = {
            "bow_id": bow_id,
            "maker": maker,
            "bow_kind": bow_kind,
            "owner": owner,
        }
    else:
        response = {"bow_id": bow_id, "maker": None, "bow_kind": None, "owner": None}

    return JSONResponse(response)
