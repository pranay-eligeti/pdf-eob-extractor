"""PDF text extraction with a deterministic fallback strategy."""

from __future__ import annotations

from pathlib import Path

import pdfplumber
import fitz


def extract_text(pdf_path: str | Path) -> str:
    path = Path(pdf_path)
    pages: list[str] = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            pages.append(page.extract_text() or "")
    text = "\n".join(pages).strip()
    if text:
        return text

    document = fitz.open(path)
    try:
        return "\n".join(page.get_text() for page in document).strip()
    finally:
        document.close()


def read_fixture(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8").strip()
