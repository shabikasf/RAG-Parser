import re
from typing import List

from app.generation.generator import Generator
from app.config import Settings
from openai import OpenAI

class OpenAIGenerator(Generator):
    def __init__(self, base_url: str, api_key: str):
        self.llm = OpenAI(base_url=base_url, api_key=api_key)

    def generate(self, query: str, context: str) -> str:

        prompt = f"""
Use ONLY the supplied context.

When using information from the context,
cite the chunk number like [Chunk 0].

If the answer is not present,
say:
'I could not find this information in the provided documents.'

Context:
{context}

Question:
{query}
"""

        response = self.llm.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content
    


    def extract_citations(self, text: str) -> List[str]:
        """
        Extract citations like:
        [Chunk 0], [Chunk 1], etc.
        """

        if not text:
            return []

        # Match [Chunk 0], [Chunk 12], etc.
        chunk_refs = re.findall(r"\[Chunk\s*(\d+)\]", text)

        # Deduplicate while preserving order
        seen = set()
        citations = []

        for c in chunk_refs:
            if c not in seen:
                seen.add(c)
                citations.append(f"Chunk {c}")

        return citations
