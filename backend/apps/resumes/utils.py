import re
from pathlib import Path

from docx import Document
from pypdf import PdfReader


SUPPORTED_RESUME_EXTENSIONS = {
    ".pdf",
    ".docx",
}


class ResumeExtractionError(ValueError):
    """
    Raised when resume text cannot be extracted safely.
    """


def extract_text_from_pdf(file):
    try:
        file.seek(0)

        reader = PdfReader(file)

        if reader.is_encrypted:
            raise ResumeExtractionError(
                "Password-protected PDF files are not supported."
            )

        pages = []

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                pages.append(
                    page_text.strip()
                )

        return "\n".join(
            pages
        ).strip()

    except ResumeExtractionError:
        raise

    except Exception as exc:
        raise ResumeExtractionError(
            "Unable to read this PDF file. "
            "Please upload a valid, non-corrupted PDF."
        ) from exc


def extract_text_from_docx(file):
    try:
        file.seek(0)

        document = Document(file)

        paragraphs = [
            paragraph.text.strip()
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        ]

        return "\n".join(
            paragraphs
        ).strip()

    except Exception as exc:
        raise ResumeExtractionError(
            "Unable to read this DOCX file. "
            "Please upload a valid, non-corrupted DOCX file."
        ) from exc


def extract_resume_text(file):
    extension = Path(
        file.name
    ).suffix.lower()

    if extension not in SUPPORTED_RESUME_EXTENSIONS:
        raise ResumeExtractionError(
            "Unsupported resume file format."
        )

    if extension == ".pdf":
        text = extract_text_from_pdf(
            file
        )
    else:
        text = extract_text_from_docx(
            file
        )

    if not text.strip():
        raise ResumeExtractionError(
            "No readable text was found in the resume. "
            "Scanned or image-only resumes are not supported yet."
        )

    return text


def normalize_text(text):
    if not text:
        return ""

    text = str(
        text
    ).lower()

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.strip()