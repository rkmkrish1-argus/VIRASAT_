"""Validate line-image/transcription pairs and build a CSV for handwriting fine-tuning.

Expected layout:
    dataset/
      train/*.png
      train/*.txt   # matching image stem; exact ground-truth transcription
      validation/*.png
      validation/*.txt

This prepares data only. It does not train a model or infer missing transcriptions.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from PIL import Image, UnidentifiedImageError

IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp"}


def collect_pairs(split_dir: Path, split_name: str) -> list[dict[str, str]]:
    if not split_dir.is_dir():
        raise ValueError(f"Missing required split folder: {split_dir}")

    rows: list[dict[str, str]] = []
    for image_path in sorted(path for path in split_dir.iterdir() if path.suffix.lower() in IMAGE_SUFFIXES):
        text_path = image_path.with_suffix(".txt")
        if not text_path.is_file():
            raise ValueError(f"Missing transcription file for {image_path.name}: expected {text_path.name}")

        try:
            with Image.open(image_path) as image:
                image.verify()
        except (OSError, UnidentifiedImageError) as error:
            raise ValueError(f"Unreadable image {image_path}: {error}") from error

        transcription = text_path.read_text(encoding="utf-8-sig").strip()
        if not transcription:
            raise ValueError(f"Transcription is empty: {text_path}")
        rows.append({"image": str(image_path.resolve()), "text": transcription, "split": split_name})

    if not rows:
        raise ValueError(f"No supported line images found in {split_dir}")
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset_dir", type=Path, help="Folder containing train/ and validation/ subfolders")
    parser.add_argument("--output", type=Path, help="CSV path (default: <dataset_dir>/manifest.csv)")
    args = parser.parse_args()

    root = args.dataset_dir.resolve()
    rows = collect_pairs(root / "train", "train") + collect_pairs(root / "validation", "validation")
    output = (args.output or root / "manifest.csv").resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8-sig", newline="") as manifest:
        writer = csv.DictWriter(manifest, fieldnames=("image", "text", "split"))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Prepared {len(rows)} labeled line images in {output}")
    print("Keep the original train/validation split; do not put crops from one page in both splits.")


if __name__ == "__main__":
    main()
