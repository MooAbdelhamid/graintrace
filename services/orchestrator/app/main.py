from app.api import router
from fastapi import FastAPI

app = FastAPI(title="Orchestrator Service")

app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok"}
