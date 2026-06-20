import logging
import fitz  # PyMuPDF
from pathlib import Path
from app.models.models import DocumentSection

logger = logging.getLogger(__name__)


def parse_pdf(file_path: str) -> list[DocumentSection]:
    logger.info(f"[PDF PARSER] Opening file: {file_path}")

    pdf = fitz.open(file_path)
    sections = []

    total_pages = len(pdf)
    logger.info(f"[PDF PARSER] Total pages: {total_pages}")

    empty_pages = 0
    extracted_pages = 0

    for page_num, page in enumerate(pdf, start=1):
        try:
            text = page.get_text().strip()
        except Exception as e:
            logger.exception(f"[PDF PARSER] Failed to extract page {page_num}: {e}")
            continue

        if not text:
            empty_pages += 1
            logger.debug(f"[PDF PARSER] Page {page_num} is empty")
            continue

        sections.append(
            DocumentSection(
                text=text,
                source_file=Path(file_path).name,
                document_type="pdf",
                metadata={
                    "page": page_num
                }
            )
        )

        extracted_pages += 1

    logger.info(
        f"[PDF PARSER] Done | extracted_pages={extracted_pages} | empty_pages={empty_pages}"
    )

    return sections