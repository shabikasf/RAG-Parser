from app.vector_store.vectorStore import VectorStore

class PineconeStore(VectorStore):

    def __init__(self):
        print("Pinecone initialized")

    def add_documents(self, chunks):
        pass

    def query(self, query: str, top_k: int = 5):
        return {
            "provider": "pinecone",
            "query": query
        }