from clients.metadata import meta_count, meta_last
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("/")
async def number_entries():

    print("Request IN")

    print("Calling Metadata")

    count = meta_count()
    last = meta_last()

    response = {
        "count": count,
        "last": last
    }

    return JSONResponse(response)
