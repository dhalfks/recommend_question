from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from io import BytesIO
import os
from pathlib import Path
import re
from uuid import uuid4

from pypdf import PdfReader

from config import settings


@dataclass(frozen=True)
class ExtractedQuestion:
    question_number: int
    content: str
    options: list[str] | None
    source_page: int


QUESTION_RE = re.compile(r"^\s*(\d{1,3})\s*[.)]\s*(.+)$")
CIRCLED_OPTION_RE = re.compile(r"^\s*([①②③④⑤])\s*(.+)$")
CIRCLED_NUMBERS = {"①": 1, "②": 2, "③": 3, "④": 4, "⑤": 5}


def extract_pdf_pages(data: bytes) -> list[str]:
    try:
        reader = PdfReader(BytesIO(data))
    except Exception as exc:
        raise ValueError("PDF 파일을 읽을 수 없습니다.") from exc
    if reader.is_encrypted:
        try:
            if reader.decrypt("") == 0:
                raise ValueError("암호화된 PDF는 등록할 수 없습니다.")
        except Exception as exc:
            raise ValueError("암호화된 PDF는 등록할 수 없습니다.") from exc
    pages = [(page.extract_text() or "").strip() for page in reader.pages]
    if not any(pages):
        raise ValueError("텍스트를 추출할 수 없습니다. 스캔 PDF는 OCR 처리 후 등록해 주세요.")
    return pages


def parse_question_candidates(pages: list[str]) -> list[ExtractedQuestion]:
    candidates: list[ExtractedQuestion] = []
    current: dict | None = None
    current_option: int | None = None

    def finish() -> None:
        nonlocal current, current_option
        if not current:
            return
        content = "\n".join(current["content"]).strip()
        options_map: dict[int, list[str]] = current["options"]
        options = None
        if len(options_map) >= 2:
            ordered = sorted(options_map)
            if ordered == list(range(1, max(ordered) + 1)):
                options = ["\n".join(options_map[index]).strip() for index in ordered]
        if content:
            candidates.append(ExtractedQuestion(
                question_number=current["number"],
                content=content,
                options=options,
                source_page=current["page"],
            ))
        current = None
        current_option = None

    for page_number, page_text in enumerate(pages, start=1):
        for raw_line in page_text.splitlines():
            line = raw_line.strip()
            if not line:
                continue
            question_match = QUESTION_RE.match(line)
            # A numbered line is an option only after a question already has content.
            option_match = CIRCLED_OPTION_RE.match(line)
            if option_match and current:
                current_option = CIRCLED_NUMBERS[option_match.group(1)]
                current["options"][current_option] = [option_match.group(2).strip()]
            elif question_match:
                finish()
                current = {"number": int(question_match.group(1)), "content": [question_match.group(2).strip()], "options": {}, "page": page_number}
            elif current and current_option is not None:
                current["options"][current_option].append(line)
            elif current:
                current["content"].append(line)
    finish()

    # Ambiguous duplicates are not imported automatically.
    counts: dict[int, int] = {}
    for item in candidates:
        counts[item.question_number] = counts.get(item.question_number, 0) + 1
    return [item for item in candidates if counts[item.question_number] == 1]


def document_sha256(data: bytes) -> str:
    return sha256(data).hexdigest()


def _storage_mode() -> str:
    mode = settings.PUBLIC_EXAM_DOCUMENT_STORAGE.lower()
    if mode == "auto":
        if settings.BLOB_READ_WRITE_TOKEN:
            return "vercel_blob"
        if os.getenv("VERCEL"):
            raise RuntimeError("Vercel 배포에서는 Private Blob 저장소 연결이 필요합니다.")
        return "local"
    if mode not in {"local", "vercel_blob"}:
        raise RuntimeError("지원하지 않는 PDF 저장 방식입니다.")
    return mode


async def store_pdf(data: bytes, original_name: str) -> str:
    safe_name = re.sub(r"[^A-Za-z0-9._-]", "_", Path(original_name).name) or "document.pdf"
    key_name = f"public-exams/{uuid4().hex}-{safe_name}"
    if _storage_mode() == "vercel_blob":
        from vercel.blob import AsyncBlobClient

        async with AsyncBlobClient(token=settings.BLOB_READ_WRITE_TOKEN or None) as client:
            result = await client.put(
                key_name,
                data,
                access="private",
                content_type="application/pdf",
                add_random_suffix=False,
            )
        return f"blob:{result.url}"

    base = Path(settings.PUBLIC_EXAM_DOCUMENT_DIR).resolve()
    destination = (base / Path(key_name).name).resolve()
    if base not in destination.parents:
        raise RuntimeError("안전하지 않은 PDF 저장 경로입니다.")
    base.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(data)
    return f"local:{destination.name}"


async def load_pdf(storage_key: str) -> bytes:
    if storage_key.startswith("blob:"):
        from vercel.blob import AsyncBlobClient

        async with AsyncBlobClient(token=settings.BLOB_READ_WRITE_TOKEN or None) as client:
            result = await client.get(storage_key.removeprefix("blob:"), access="private")
        return result.content
    if storage_key.startswith("local:"):
        base = Path(settings.PUBLIC_EXAM_DOCUMENT_DIR).resolve()
        source = (base / storage_key.removeprefix("local:")).resolve()
        if base not in source.parents or not source.is_file():
            raise FileNotFoundError("PDF 파일을 찾을 수 없습니다.")
        return source.read_bytes()
    raise FileNotFoundError("지원하지 않는 PDF 저장 키입니다.")


async def delete_pdf(storage_key: str) -> None:
    if storage_key.startswith("blob:"):
        from vercel.blob import AsyncBlobClient

        async with AsyncBlobClient(token=settings.BLOB_READ_WRITE_TOKEN or None) as client:
            await client.delete(storage_key.removeprefix("blob:"))
    elif storage_key.startswith("local:"):
        base = Path(settings.PUBLIC_EXAM_DOCUMENT_DIR).resolve()
        source = (base / storage_key.removeprefix("local:")).resolve()
        if base in source.parents and source.is_file():
            source.unlink()
