import re
from pathlib import Path

from docx import Document
from pypdf import PdfReader


def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text.strip()


def extract_text_from_docx(file):
    document = Document(file)

    paragraphs = []

    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            paragraphs.append(
                paragraph.text
            )

    return "\n".join(
        paragraphs
    ).strip()


def extract_resume_text(file):
    extension = Path(
        file.name
    ).suffix.lower()

    if extension == ".pdf":
        return extract_text_from_pdf(
            file
        )

    if extension == ".docx":
        return extract_text_from_docx(
            file
        )

    raise ValueError(
        "Unsupported resume file format."
    )


def normalize_text(text):
    if not text:
        return ""

    text = str(text).lower()

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.strip()