from abc import ABC, abstractmethod
from app.models.models import DocumentSection

class VectorStore(ABC):
    @abstractmethod
    def add_documents(self, sections: list[DocumentSection]):
        pass

    @abstractmethod
    def query(self, query: str, top_k: int = 5) -> list[DocumentSection]:
        pass