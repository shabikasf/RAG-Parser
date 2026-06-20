from fastapi import APIRouter, Request, UploadFile, File, HTTPException
from app.models.models import IngestResponse
from app.ingestion.ingestion_service import IngestionService

from pathlib import Path

tmp_dir = Path("tmp")
tmp_dir.mkdir(exist_ok=True)

file_path = tmp_dir

router = APIRouter()

@router.post("/ingest", response_model=list[IngestResponse])
async def ingest( request: Request, files: list[UploadFile] = File(...)):
    file_paths = []
    for file in files:
        try:
            contents = await file.read()
            path = file_path / file.filename
            with open(path, "wb") as f:
                f.write(contents)
            file_paths.append(path)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to save {file.filename}: {str(e)}")

    ingestion_service: IngestionService = request.app.state.container.ingestion_service
    results = ingestion_service.ingest_files(file_paths)

    return results