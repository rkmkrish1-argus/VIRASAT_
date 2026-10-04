"""Download fast Tesseract language models into the local archive data folder."""

from __future__ import annotations

from pathlib import Path
from urllib.request import Request, urlopen


PROJECT_ROOT = Path(__file__).resolve().parent.parent
TESSDATA_DIR = PROJECT_ROOT / "ambedkar_archive_data" / "ocr_models" / "tessdata"
LANGUAGES = ("eng", "hin", "mar", "tam", "tel", "ben", "guj", "pan", "mal", "kan", "osd")
BASE_URL = "https://raw.githubusercontent.com/tesseract-ocr/tessdata_fast/main"
USER_AGENT = "AmbedkarHeritageArchive/1.0 OCR language-data setup"


def main() -> None:
    TESSDATA_DIR.mkdir(parents=True, exist_ok=True)
    for language in LANGUAGES:
        destination = TESSDATA_DIR / f"{language}.traineddata"
        if destination.is_file() and destination.stat().st_size > 0:
            print(f"Already available: {language}")
            continue

        request = Request(f"{BASE_URL}/{language}.traineddata", headers={"User-Agent": USER_AGENT})
        temporary = destination.with_suffix(".traineddata.download")
        try:
            with urlopen(request, timeout=90) as response, temporary.open("wb") as output:
                output.write(response.read())
            if temporary.stat().st_size < 100_000:
                raise RuntimeError(f"Downloaded language data for {language} is unexpectedly small.")
            temporary.replace(destination)
            print(f"Installed: {language}")
        except Exception:
            temporary.unlink(missing_ok=True)
            raise

    print(f"Tesseract language data is ready in {TESSDATA_DIR}")


if __name__ == "__main__":
    main()
