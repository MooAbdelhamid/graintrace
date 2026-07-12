from clients.metadata import meta_count
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("/")
async def number_enteries():

    print("Request IN")

    print("Calling Metadata")

    response = meta_count()

    return JSONResponse(response)
