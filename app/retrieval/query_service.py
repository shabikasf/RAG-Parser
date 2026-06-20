from app.vector_store.vectorStore import VectorStore


class QueryService:

    def __init__(
        self,
        vector_store: VectorStore,
        llm
    ):
        self.vector_store = vector_store
        self.llm = llm

    def query(self, question: str):

        retrieved = self.vector_store.query(
            question,
            top_k=5
        )

        context = self.build_context(retrieved)

        answer = self.llm.generate(
            query=question,
            context=context
        )

        citations = self.llm.extract_citations(
            answer
        )

        return {
            "answer": answer,
            "citations": citations
        }
    
    def build_context(self, results):
        docs = results["documents"][0]
        metas = results.get("metadatas", [[]])[0]

        context_parts = []

        for i, (doc, meta) in enumerate(zip(docs, metas)):
            source = meta.get("source_file", "unknown")
            page = meta.get("page", "NA")
            section = meta.get("section", "NA")

            context_parts.append(
                f"""[Chunk {i}]
    Source: {source} | Page: {page} | Section: {section}
    Content:
    {doc}
    """
            )

        return "\n\n".join(context_parts)
