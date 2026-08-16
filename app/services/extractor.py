import io

import trafilatura
from pypdf import PdfReader

MAX_PDF_PAGES = 40


def is_url(text: str) -> bool:
    stripped = text.strip()
    return stripped.startswith("http://") or stripped.startswith("https://")


def extract_from_url(url: str) -> str:
    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        raise ValueError("Не вдалося завантажити сторінку за цим посиланням.")
    text = trafilatura.extract(downloaded)
    if not text:
        raise ValueError("Не вдалося знайти текст на цій сторінці.")
    return text


def extract_from_pdf(file_bytes: bytes) -> str:
    reader = PdfReader(io.BytesIO(file_bytes))
    pages = reader.pages[:MAX_PDF_PAGES]
    text = "\n".join(page.extract_text() or "" for page in pages)
    if not text.strip():
        raise ValueError("Не вдалося витягнути текст із цього PDF (можливо, це скан-зображення).")
    return text
