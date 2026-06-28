from app.api import router
from fastapi import FastAPI

app = FastAPI(title="Metadata Service")

app.include_router(router)


@app.get("/health")
async def health():
    return {"status": "ok"}
