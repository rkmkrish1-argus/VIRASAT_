# Ambedkar Digital Heritage Archive — Local MVP

## What is included

- React + Vite archive interface
- Node.js + Express API
- Local JSON metadata database
- Upload PDF/JPG/PNG/TXT files
- Archive metadata
- Search across title, author, description, OCR/search text and tags
- Collection filter
- Document detail viewer
- Delete record
- Sample Ambedkar archive records
- Responsive UI

## Requirements

Install Node.js 20+.

Check:

```bash
node -v
npm -v
```

## Install

From this project folder:

```bash
npm run install-all
```

## Start

```bash
npm run dev
```

Open:

http://localhost:5173

API:

http://localhost:5000/api/health

## Test

1. Search for `Ambedkar`.
2. Search for `constitution`.
3. Open a record.
4. Click `Upload Record`.
5. Add metadata and optionally upload a PDF/image/text file.
6. Search for text you entered in the OCR/Searchable Text field.
7. Open the record and test the file link.
8. Delete a test record.

## Important

This is a development MVP. The sample records are placeholders for testing the software pipeline. Before public deployment, replace them with verified archival material and add authentication, provenance, rights metadata, OCR processing, backups, audit logs and production database/search infrastructure.

## Next production modules

1. PostgreSQL
2. Object storage
3. Tesseract/PaddleOCR
4. Human OCR review
5. Elasticsearch/OpenSearch
6. Multilingual OCR
7. IIIF image/document delivery
8. Semantic/vector search
9. Role-based admin
10. Provenance and rights management
