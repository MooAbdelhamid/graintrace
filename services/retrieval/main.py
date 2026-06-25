from app.api import router
from config import config
from fastapi import FastAPI

app = FastAPI(title="Retrieval Service")

# create qdrant collection on startup if it does not exist

app.include_router(router)


@app.get("/health")
async def health():
    return {"status": "ok", "collection": config.COLLECTION_NAME}
