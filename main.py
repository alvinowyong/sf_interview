import time
import os

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator

from api import v1_router
from api.models import HealthResponse, ReadRootResponse

app = FastAPI(
    title="Interview challenge",
    version="0.1.0",
    description="Implementation for the interview challenge",
)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

# Prometheus instrumentor 
Instrumentator().instrument(app).expose(app, endpoint="/metrics")

# Root path
@app.get("/", response_model=ReadRootResponse)
async def read_root():
    read_result = ReadRootResponse(
        version=app.version,
        date=int(time.time()),
        kubernetes=("KUBERNETES_SERVICE_HOST" in os.environ)
    )
    return read_result

# Prometheus health endpoint
@app.get("/health", response_model=HealthResponse)
async def health():
    return {"message": "ok"}

app.include_router(v1_router, prefix="/v1")

if __name__ == "__main__":
    # Default log_level="info" provides access logs for the service
    uvicorn.run("main:app", host="0.0.0.0", port=3000, log_level="info", reload=True)
