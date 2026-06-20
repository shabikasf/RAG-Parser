import magic
import msoffcrypto
from PyPDF2 import PdfReader

from app.exceptions import PasswordProtectedError
from app.models.models import DocumentSection

from pathlib import Path

import logging

logger = logging.getLogger(__name__)

SUPPORTED_EXTENSIONS = {"pdf", "docx", "pptx", "xlsx"}

def detect_file_type(path: str) -> str:
    return Path(path).suffix.lower().lstrip(".")

def check_file_type(path: str) -> str:
    p = Path(path)

    print("DEBUG path:", p.resolve())
    print("EXISTS:", p.exists())

    if not p.exists():
        raise FileNotFoundError(f"File not found: {p}")

    mime = magic.Magic(mime=True)
    file_type = mime.from_file(str(p))
    print("RAW MIME:", file_type)
    return file_type

def is_password_protected(ext: str, path: str) -> bool:

    try:
        if ext == "pdf":
            return PdfReader(path).is_encrypted

        elif ext in ["docx", "xlsx", "pptx"]:
            with open(path, "rb") as f:
                return msoffcrypto.OfficeFile(f).is_encrypted()

        else:
            raise ValueError(f"Unsupported file type: {ext}")

    except Exception as e:
        print(f"Error checking {path}: {e}")
        return False

class UnsupportedFileTypeError(Exception):
    pass

def validate_file(path: str) -> str:
    ext = detect_file_type(path)

    if ext not in SUPPORTED_EXTENSIONS:
        raise UnsupportedFileTypeError(f"Unsupported file type: {ext}")

    return ext