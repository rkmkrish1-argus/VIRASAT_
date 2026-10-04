from io import BytesIO
import math
import os
from pathlib import Path
import shutil
from typing import Tuple

import pymupdf
import pytesseract
from PIL import Image, ImageOps, UnidentifiedImageError
from pytesseract import TesseractError, TesseractNotFoundError

MAX_UPLOAD_BYTES = 20 * 1024 * 1024
MAX_PDF_PAGES = 50
MAX_IMAGE_PIXELS = 40_000_000
PDF_RENDER_SCALE = 300 / 72
HANDWRITTEN_MODEL = "ambedkar_handwritten_v2"
OCR_MODES = {"printed", "handwritten"}

TESSERACT_LANGUAGES = {
    "en": "eng",
    "hi": "hin",
    "mr": "mar",
    "ta": "tam",
    "te": "tel",
    "bn": "ben",
    "gu": "guj",
    "pa": "pan",
    "ml": "mal",
    "kn": "kan",
}


def _configure_tesseract() -> tuple[str, str]:
    """Find the OCR engine and its trained-data folder on Windows and other hosts."""
    configured_command = os.getenv("TESSERACT_CMD", "").strip()
    candidates = [Path(configured_command)] if configured_command else []

    local_app_data = os.getenv("LOCALAPPDATA")
    program_files = os.getenv("ProgramFiles", r"C:\Program Files")
    if local_app_data:
        candidates.append(Path(local_app_data) / "Programs" / "Tesseract-OCR" / "tesseract.exe")
    candidates.extend([
        Path(program_files) / "Tesseract-OCR" / "tesseract.exe",
        Path(r"C:\Program Files (x86)") / "Tesseract-OCR" / "tesseract.exe",
    ])

    path_command = shutil.which("tesseract")
    if path_command:
        candidates.append(Path(path_command))

    for candidate in candidates:
        if candidate.is_file():
            pytesseract.pytesseract.tesseract_cmd = str(candidate)
            tessdata_dir = os.getenv("TESSDATA_PREFIX", "").strip()
            if not tessdata_dir:
                adjacent = candidate.parent / "tessdata"
                if adjacent.is_dir():
                    tessdata_dir = str(adjacent)
            return str(candidate), tessdata_dir

    # Leave PATH-based lookup enabled so the normal pytesseract error is preserved.
    pytesseract.pytesseract.tesseract_cmd = configured_command or "tesseract"
    return pytesseract.pytesseract.tesseract_cmd, os.getenv("TESSDATA_PREFIX", "").strip()


TESSERACT_CMD, TESSDATA_DIR = _configure_tesseract()

PROJECT_TESSDATA_DIR = Path(__file__).resolve().parent.parent / "ambedkar_archive_data" / "ocr_models" / "tessdata"
configured_tessdata_dir = os.getenv("ARCHIVE_OCR_TESSDATA_DIR", "").strip()
if configured_tessdata_dir and Path(configured_tessdata_dir).is_dir():
    TESSDATA_DIR = configured_tessdata_dir
elif PROJECT_TESSDATA_DIR.is_dir() and any(PROJECT_TESSDATA_DIR.glob("*.traineddata")):
    TESSDATA_DIR = str(PROJECT_TESSDATA_DIR)

if TESSDATA_DIR:
    # Tesseract reads this environment variable reliably on Windows; passing a
    # quoted --tessdata-dir through pytesseract's Windows argument parser keeps
    # the quotes in the argument and makes Tesseract look in the wrong folder.
    os.environ["TESSDATA_PREFIX"] = TESSDATA_DIR


def _tesseract_config() -> str:
    return ""


class OCRInputError(Exception):
    pass


class OCRLanguageError(Exception):
    pass


class OCRUnavailableError(Exception):
    pass


class OCRModelUnavailableError(OCRUnavailableError):
    pass


def handwritten_model_status() -> dict[str, str | bool]:
    """Report whether the custom Tesseract handwriting model is installed."""
    model_path = PROJECT_TESSDATA_DIR / f"{HANDWRITTEN_MODEL}.traineddata"
    try:
        installed_languages = pytesseract.get_languages(config="")
    except (TesseractNotFoundError, TesseractError) as error:
        return {
            "model": HANDWRITTEN_MODEL,
            "installed": False,
            "path": str(model_path),
            "message": f"Tesseract is unavailable: {error}",
        }

    installed = HANDWRITTEN_MODEL in installed_languages
    return {
        "model": HANDWRITTEN_MODEL,
        "installed": installed,
        "path": str(model_path),
        "message": (
            "Custom handwriting OCR model is ready."
            if installed
            else f"Model file is missing. Place {HANDWRITTEN_MODEL}.traineddata in {PROJECT_TESSDATA_DIR}."
        ),
    }


def _recognize(image: Image.Image, language: str, mode: str = "printed") -> str:
    config = "--oem 1 --psm 6" if mode == "handwritten" else _tesseract_config()
    try:
        return pytesseract.image_to_string(image, lang=language, config=config)
    except TesseractNotFoundError as error:
        raise OCRUnavailableError("Tesseract OCR is not installed or is not on PATH.") from error
    except TesseractError as error:
        raise OCRInputError(f"Tesseract could not process the document: {error}") from error


def extract_text(file_name: str, content: bytes, language: str, mode: str = "printed") -> Tuple[str, int]:
    if not content:
        raise OCRInputError("The uploaded file is empty.")
    if len(content) > MAX_UPLOAD_BYTES:
        raise OCRInputError("Files must be 20 MB or smaller.")

    extension = Path(file_name).suffix.lower()
    if extension not in {".pdf", ".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp", ".webp"}:
        raise OCRInputError("Upload a PDF, PNG, JPEG, TIFF, BMP, or WEBP file.")

    if mode not in OCR_MODES:
        raise OCRInputError("OCR mode must be 'printed' or 'handwritten'.")

    if mode == "handwritten":
        status = handwritten_model_status()
        if not status["installed"]:
            raise OCRModelUnavailableError(str(status["message"]))
        tess_language = HANDWRITTEN_MODEL
    else:
        tess_language = TESSERACT_LANGUAGES.get(language)
        if not tess_language:
            raise OCRLanguageError(f"OCR is not configured for language '{language}'.")

    try:
        installed_languages = pytesseract.get_languages(config=_tesseract_config())
    except TesseractNotFoundError as error:
        raise OCRUnavailableError("Tesseract OCR is not installed or is not on PATH.") from error

    if tess_language not in installed_languages:
        raise OCRLanguageError(
            f"Tesseract language data '{tess_language}' is not installed. "
            "Install that traineddata pack and try again."
        )

    if extension == ".pdf":
        try:
            document = pymupdf.open(stream=content, filetype="pdf")
        except (pymupdf.FileDataError, ValueError) as error:
            raise OCRInputError("The uploaded PDF is invalid or could not be opened.") from error

        with document:
            if document.page_count > MAX_PDF_PAGES:
                raise OCRInputError(f"PDFs are limited to {MAX_PDF_PAGES} pages per upload.")

            page_text = []
            for page in document:
                width = math.ceil(page.rect.width * PDF_RENDER_SCALE)
                height = math.ceil(page.rect.height * PDF_RENDER_SCALE)
                if width * height > MAX_IMAGE_PIXELS:
                    raise OCRInputError("A PDF page is too large to process safely.")

                pixmap = page.get_pixmap(
                    matrix=pymupdf.Matrix(PDF_RENDER_SCALE, PDF_RENDER_SCALE),
                    colorspace=pymupdf.csRGB,
                    alpha=False,
                )
                image = Image.frombytes("RGB", (pixmap.width, pixmap.height), pixmap.samples)
                page_text.append(_recognize(image, tess_language, mode).strip())

            return "\n\n".join(text for text in page_text if text), document.page_count

    try:
        with Image.open(BytesIO(content)) as source_image:
            image = ImageOps.exif_transpose(source_image)
            if image.width * image.height > MAX_IMAGE_PIXELS:
                raise OCRInputError("The uploaded image is too large to process safely.")
            text = _recognize(image.convert("RGB"), tess_language, mode)
    except UnidentifiedImageError as error:
        raise OCRInputError("The uploaded image is invalid or could not be opened.") from error

    return text.strip(), 1
