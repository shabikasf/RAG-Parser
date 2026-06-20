from fastapi import Request
from app.config import Settings


def get_settings(request: Request) -> Settings:
    """
    Returns app settings stored during FastAPI startup.
    """
    return request.app.state.settings


def get_vector_store(request: Request):
    """
    Returns the initialized VectorStore instance (Chroma / Pinecone).
    """
    return request.app.state.vector_store