from app.bulk_register import router as bulk_register_router
from app.delete import router as delete_router
from app.register import router as register_router
from app.stats import router as stats_router
from app.verify import router as verify_router
from fastapi import FastAPI

app = FastAPI(title="Orchestrator Service")

app.include_router(verify_router)

app.include_router(register_router)

app.include_router(bulk_register_router)

app.include_router(delete_router)

app.include_router(stats_router)


@app.get("/health")
async def health():
    return {"status": "ok"}
