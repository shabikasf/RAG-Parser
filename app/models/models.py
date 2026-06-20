from pydantic import BaseModel, Field
from typing import Optional


class DocumentSection(BaseModel):
    text: str

    source_file: str
    document_type: str

    page: Optional[int] = None
    section: Optional[str] = None
    sheet: Optional[str] = None

    metadata: dict = Field(default_factory=dict)

class Chunk(BaseModel):
    id: str
    text: str

    source_file: str
    document_type: str

    chunk_index: int

    page: Optional[int] = None
    section: Optional[str] = None
    sheet: Optional[str] = None

    metadata: dict = Field(default_factory=dict)

class Citation(BaseModel):
    source_file: str
    page: int | None = None
    section: str | None = None

class QueryResult(BaseModel):
    text: str
    source_file: str
    document_type: str

    page: Optional[int] = None
    section: Optional[str] = None
    sheet: Optional[str] = None

    metadata: dict = Field(default_factory=dict)

class IngestResponse(BaseModel):
    file: str
    status: str
    chunks: Optional[int] = None
    reason: Optional[str] = None

class QueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5
    filters: Optional[dict] = None

class QueryResponse(BaseModel):
    query: str
    answer: str
    citations: list[QueryResult]