# Handwriting OCR training plan

## Current capability

The archive currently uses Tesseract's downloaded language models for printed text. Those language packs support printed OCR; they are not a model trained on handwriting. A scanned handwritten page can therefore produce poor or empty results, especially when it is cursive, crossed out, faint, skewed, or contains multiple columns.

The supplied sample is one English cursive manuscript page with substantial strike-throughs. It is useful as a representative evaluation example, but it is not enough to train a general handwriting recognizer, and it has no verified transcription paired with it. No handwriting model has been trained yet.

## What is required to train it

Handwriting models need image samples paired with exact human-checked text. For a line recognizer, each image should contain one cropped text line and a matching UTF-8 `.txt` file with the transcription. Include examples from the target scripts, handwriting styles, eras, scan quality, and page layouts. Keep pages from the same source document in only one data split, so near-identical lines cannot leak from training into validation.

For historical pages, agree on transcription rules before labeling:

- whether crossed-out words are omitted, retained, or marked (for example `[crossed out: word]`);
- how uncertain characters, abbreviations, punctuation, and line breaks are represented;
- whether the transcript is diplomatic (preserves original spelling) or normalized.

English, Hindi, and Marathi handwriting require suitable script/token support and labeled examples for each. One English cursive sample cannot teach the model Devanagari or every writer's style. This project does not claim universal handwriting accuracy.

## Prepare labeled line data

Create this folder layout. Each image must be a single text line; its `.txt` file must have the same base name.

```text
handwriting_dataset/
  train/
    page001_line001.png
    page001_line001.txt
  validation/
    page020_line001.png
    page020_line001.txt
```

Run the included pair validator and manifest builder:

```powershell
python backend/prepare_handwriting_data.py handwriting_dataset
```

It checks that image/transcription pairs exist and are readable, then writes `handwriting_dataset/manifest.csv`. It does not invent labels or train a model. Store scans only when the institution has permission to use them for OCR development.

## Model direction

The official Microsoft TrOCR handwritten checkpoints are line-image recognizers and are a reasonable starting point for an English handwritten prototype. They do not solve whole-page layout analysis or multilingual handwriting by themselves. A production path needs line/region segmentation, script-specific model selection or fine-tuning, a held-out evaluation set, and a review step for low-confidence output. The current `/api/ocr` endpoint remains the Tesseract printed-text path until a handwriting model is trained and integrated.

## Evaluation before enabling for archival ingestion

Keep a held-out set of complete pages from writers/documents absent from training. Report character error rate (CER) and word error rate (WER) separately for each language, script, and scan condition. Inspect strike-through, marginalia, names, dates, and punctuation errors manually. OCR output from uncertain historical text must be reviewed by a person before it is added to the searchable archive.

## What is needed to continue

Provide line-cropped images and their verified transcriptions for each target script, or a source corpus that can legally be annotated. Also choose whether crossed-out words should be transcribed. Once a labeled set exists, fine-tune an appropriate line recognizer and evaluate it before connecting it to the archive's upload flow.
