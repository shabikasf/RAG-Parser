import json

from app.chunking.chunk import build_chunks
from app.ingestion.detection import validate_file
from app.ingestion.parser_register import get_parser
from app.models.models import IngestResponse

import logging
logger = logging.getLogger(__name__)

class IngestionService:

    def __init__(self, vector_store):
        self.vector_store = vector_store

    def ingest_files(self, paths: list[str]) -> list[IngestResponse]:
        results = []

        for path in paths:
            try:
                logger.info(f"[INGEST] Processing file: {path}")

                ext = validate_file(path)
                logger.info(f"[INGEST] Detected extension: {ext}")

                parser = get_parser(ext)
                logger.info(f"[INGEST] Selected parser: {parser.__name__}")

                sections = parser(path)
                logger.info(f"[INGEST] Parsed sections: {len(sections)} {json.dumps([s.metadata for s in sections], indent=2)}")

                chunks = build_chunks(sections)
                logger.info(f"[INGEST] Built chunks: {len(chunks)}")

                self.vector_store.add_documents(chunks)

                results.append(IngestResponse(
                    file=str(path),
                    status="success",
                    chunks=len(chunks)
                ))

            except Exception as e:
                logger.exception(f"[INGEST] Failed for file: {path}")

                results.append(IngestResponse(
                    file=str(path),
                    status="failed",
                    reason=str(e)
                ))

        return results