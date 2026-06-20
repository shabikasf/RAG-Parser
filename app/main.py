import uvicorn

from fastapi import FastAPI
from app.container import Container
from app.config import Settings
from app.api.query import app as query_router
from app.api.ingest import router as ingest_router

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

app = FastAPI()

@app.on_event("startup")
def startup():
    settings = Settings()
    app.state.container = Container(settings)

app.include_router(query_router, prefix="/api")
app.include_router(ingest_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)