"""File ingestion helpers for the health report workflow."""
from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Iterable

import pdfplumber
from docx import Document

SUPPORTED_SUFFIXES = {".doc", ".docx", ".pdf"}


class IngestionError(RuntimeError):
    """Raised when a source report cannot be parsed."""


def _read_docx(path: Path) -> str:
    document = Document(path)
    return "\n".join(paragraph.text.strip() for paragraph in document.paragraphs if paragraph.text.strip())


def _read_pdf(path: Path) -> str:
    text_lines: list[str] = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            if page_text:
                text_lines.append(page_text)
    return "\n".join(text_lines)


def _convert_doc_to_docx(path: Path) -> Path:
    """Convert a legacy .doc file into .docx via LibreOffice."""

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        cmd = [
            "soffice",
            "--headless",
            "--convert-to",
            "docx",
            str(path),
            "--outdir",
            str(tmp_path),
        ]
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except FileNotFoundError as exc:  # pragma: no cover - depends on environment
            raise IngestionError("LibreOffice (soffice) is required to convert .doc files.") from exc
        except subprocess.CalledProcessError as exc:  # pragma: no cover - depends on input data
            raise IngestionError(f"Failed to convert {path} to docx: {exc.stderr.decode(errors='ignore')}") from exc

        converted = next(tmp_path.glob("*.docx"), None)
        if not converted:
            raise IngestionError(f"Conversion produced no docx for {path}.")
        target = path.with_suffix(".converted.docx")
        shutil.move(str(converted), target)
        return target


def load_text(path: Path) -> tuple[str, Path]:
    """Load text content from a report file.

    Returns a tuple containing the extracted text and the path that was
    ultimately read (useful if .doc files were converted).
    """

    suffix = path.suffix.lower()
    if suffix not in SUPPORTED_SUFFIXES:
        raise IngestionError(f"Unsupported file type: {path.suffix}")

    if suffix == ".pdf":
        return _read_pdf(path), path

    actual_path = path
    if suffix == ".doc":
        actual_path = _convert_doc_to_docx(path)

    return _read_docx(actual_path), actual_path


def load_many(paths: Iterable[Path]) -> dict[str, tuple[str, Path]]:
    """Bulk load report files into a mapping keyed by stem."""

    loaded: dict[str, tuple[str, Path]] = {}
    for path in paths:
        text, actual_path = load_text(path)
        loaded[path.stem] = (text, actual_path)
    return loaded
