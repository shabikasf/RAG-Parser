import logging
import uuid
from typing import List
import tiktoken

from app.models.models import Chunk, DocumentSection

logger = logging.getLogger(__name__)

encoding = tiktoken.get_encoding("cl100k_base")


def build_chunks(sections: List[DocumentSection]) -> List[Chunk]:
    all_chunks = []

    logger.info(f"[CHUNK BUILDER] Starting chunking for {len(sections)} sections")

    for s_idx, section in enumerate(sections):
        text_len = len(section.text or "")

        logger.info(
            f"[CHUNK BUILDER] Section {s_idx} | file={section.source_file} | chars={text_len}"
        )

        text_chunks = split_tokens(section.text)

        logger.info(
            f"[CHUNK BUILDER] Section {s_idx} produced {len(text_chunks)} chunks"
        )

        for i, chunk_text in enumerate(text_chunks):

            # 🚨 safety check for empty chunks
            if not chunk_text.strip():
                logger.warning(
                    f"[CHUNK BUILDER] Skipping empty chunk | section={s_idx} | chunk={i}"
                )
                continue

            meta = {
                **(section.metadata or {}),
                "section_title": section.section
            }

            # 🚨 log suspicious metadata
            for k, v in meta.items():
                if v is None:
                    logger.debug(
                        f"[CHUNK META] None value | key={k} | section={s_idx} | chunk={i}"
                    )

            chunk_id = str(uuid.uuid4())

            logger.debug(
                f"[CHUNK BUILDER] Creating chunk | id={chunk_id} | section={s_idx} | chunk={i}"
            )

            all_chunks.append(
                Chunk(
                    id=chunk_id,
                    text=chunk_text,

                    source_file=section.source_file,
                    document_type=section.document_type,

                    chunk_index=i,

                    page=section.page,
                    section=section.section,
                    sheet=section.sheet,

                    metadata=meta
                )
            )

    logger.info(f"[CHUNK BUILDER] Total chunks created: {len(all_chunks)}")

    return all_chunks


def split_tokens(text: str, chunk_size: int = 500, overlap: int = 100):
    tokens = encoding.encode(text)

    logger.debug(f"[TOKEN SPLIT] Total tokens: {len(tokens)}")

    chunks = []
    start = 0

    chunk_id = 0

    while start < len(tokens):
        end = start + chunk_size
        chunk = tokens[start:end]

        decoded = encoding.decode(chunk)

        logger.debug(
            f"[TOKEN SPLIT] Chunk {chunk_id} | tokens={len(chunk)}"
        )

        chunks.append(decoded)

        start = end - overlap
        chunk_id += 1

    return chunks