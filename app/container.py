from app.vector_store.factory import get_vector_store
from app.generation.factory import get_generator
from app.ingestion.ingestion_service import IngestionService
from app.retrieval.query_service import QueryService


class Container:

    def __init__(self, settings):

        self.vector_store = get_vector_store(settings)

        self.generator = get_generator(settings)

        self.ingestion_service = IngestionService(
            self.vector_store
        )

        self.query_service = QueryService(
            self.vector_store,
            self.generator
        )