from sentence_transformers import SentenceTransformer

from app.embeddings.embedder import Embedder


class SentenceTransformerEmbedder(Embedder):

    def __init__(self):
        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    def embed(self, texts: list[str]) -> list[list[float]]:
        return self.model.encode(
            texts,
            normalize_embeddings=True
        ).tolist()