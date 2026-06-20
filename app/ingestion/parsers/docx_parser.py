from docx import Document
from pathlib import Path

from app.models.models import DocumentSection


def parse_docx(file_path: str) -> list[DocumentSection]:
    doc = Document(file_path)

    sections = []

    current_heading = Path(file_path).stem
    current_content = []

    for paragraph in doc.paragraphs:

        text = paragraph.text.strip()

        if not text:
            continue

        style_name = paragraph.style.name.lower()

        if style_name.startswith("heading"):

            if current_content:
                sections.append(
                    DocumentSection(
                        text="\n".join(current_content),
                        source_file=Path(file_path).name,
                        document_type="docx",
                        metadata={
                            "heading": current_heading
                        }
                    )
                )

            current_heading = text
            current_content = []

        else:
            current_content.append(text)

    if current_content:
        sections.append(
            DocumentSection(
                text="\n".join(current_content),
                source_file=Path(file_path).name,
                document_type="docx",
                metadata={
                    "heading": current_heading
                }
            )
        )

    return sections