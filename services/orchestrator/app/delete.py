from clients.metadata import meta_delete
from clients.retrieval import retrieval_delete
from fastapi import APIRouter, Path
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/delete", tags=["delete"])


@router.delete("/{bow_id}")
async def delete(bow_id: str = Path(..., description="The bow_id to delete")):

    print("Request IN")

    print("Calling Retrieval")

    retrieval_result = retrieval_delete(bow_id)

    if retrieval_result["status"] != "deleted":
        return {"status": "failed", "message": "failed to delete from embeddings db"}

    print("Calling Metadata")

    metadata_result = meta_delete(bow_id)

    if metadata_result["status"] != "deleted":
        return JSONResponse(
            {"status": "failed", "message": "failed to delete from metadata db"}
        )

    response = {"status": "success",
                "bow_id": bow_id,
                "message": f"{bow_id} deleted successfully",
                }

    return JSONResponse(response)
