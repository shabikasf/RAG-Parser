from app.config import Settings
from app.vector_store.chromaStore import ChromaStore
from app.vector_store.pineconeStore import PineconeStore

def get_embedder(settings: Settings):
    """
    Factory function that returns the correct Embedder implementation
    based on config.
    """

    embedder_type = settings.embedder_type.lower()

    if embedder_type == "sentence_transformer":
        from app.embeddings.sentence_transformer_embedder import SentenceTransformerEmbedder
        return SentenceTransformerEmbedder()

    raise ValueError(f"Unsupported embedder type: {embedder_type}")


def get_vector_store(settings: Settings):
    """
    Factory function that returns the correct VectorStore implementation
    based on config.
    """

    store_type = settings.vector_store_type.lower()

    if store_type == "chroma":
        embedder = get_embedder(settings)
        return ChromaStore(embedder=embedder)

    if store_type == "pinecone":
        return PineconeStore(
            api_key=settings.pinecone_api_key,
            index_name=settings.pinecone_index
        )

    raise ValueError(f"Unsupported vector store type: {store_type}")