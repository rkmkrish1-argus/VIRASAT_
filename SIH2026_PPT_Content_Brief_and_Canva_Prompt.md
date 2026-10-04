# SIH 2026 Idea Presentation: Project Brief and Canva Prompt

**Purpose:** Give a Canva AI or presentation creator the project facts, dataset and database details, the uploaded SIH template requirements, and a copy-ready prompt for preparing the SIH idea presentation.

**Prepared from:** `SIH2026-IDEA-Presentation-Format.pptx`, `sih_2026_ppt_layout_and_creator_notes.md`, and the project source/data files in this repository. Project files and inventory were reviewed on **30 September 2026**.

## Read this first

Use these sources in this order:

1. **The uploaded SIH PowerPoint template controls the slide structure and submission rules.** It requires no more than six slides including the title, says to keep the supplied template and its idea-detail pointers, and says to submit a PDF. The template contains a seventh “Important Instructions” slide; use it as guidance, then remove it from the final six-slide submission.
2. **This Markdown file is the source of project facts.** It distinguishes what the repository contains from what is only proposed.
3. **The creator-notes file is secondary advice from a video.** It is not a substitute for the uploaded template and must not override it.

Do not invent the official problem statement title, team ID, team name, costs, hardware models, deployment results, user research, research citations, or performance results. Use clearly marked placeholders for missing team/portal details and ask the team to fill them in.

## SIH identity and fields

| Field | Verified project information |
|---|---|
| Problem Statement ID | **26096** (project README and data inventory) |
| Working project title | **Dr. B. R. Ambedkar Digital Heritage Archive** |
| Project description in README | “AI-Powered Institutional Archive & Audio-Visual Knowledge Platform” (use as the solution description, not as a verified official SIH problem title) |
| Issuing authority / ministry | Ministry of Social Justice and Empowerment (MoSJE), as stated in project files |
| Primary institution | Dr. Ambedkar International Centre (DAIC), as stated in project files |
| Theme | **Smart Education**, as stated in the README |
| Category | **Hardware (with Integrated Software)**, as stated in the README; the template’s field says “Software/Hardware” |
| Team ID | **[FILL FROM SIH PORTAL]** |
| Registered team name | **[FILL EXACTLY AS ON SIH PORTAL]** |
| Official problem statement title | **[VERIFY AND COPY EXACTLY FROM SIH PORTAL]** |

## What the uploaded template requires

The rendered template is widescreen **16:9** and has a white background, blue headings/footer, SIH 2026 logo, and slide-number footer. Preserve the provided template’s visual design, logos, title placeholders, slide order, and required idea-detail points. Keep the final deck to six slides maximum, including the cover.

| Final slide | Template heading | Required content from template |
|---|---|---|
| 1 | Title page | Problem Statement ID and title, theme, PS category, team ID, registered team name |
| 2 | Proposed Solution | Explanation of the proposed solution, how it addresses the problem, and its innovation/uniqueness |
| 3 | Technical Approach | Technologies/components (including hardware), plus a clear implementation method or flow diagram/prototype |
| 4 | Feasibility and Viability | Feasibility, risks/challenges, and mitigation strategies |
| 5 | Impact and Benefits | Target audience and expected social, economic, environmental, or other benefits |
| 6 | Research and References | Real research/reference details and links |

The template’s seventh slide says:

- Six slides maximum, **including the title slide**.
- Prefer concise points, diagrams, infographics, and useful pictures over paragraphs.
- Keep explanations precise and easy to understand.
- Keep the supplied template and the idea-detail pointers.
- Save and submit **PDF**; the template says PPT, Word, and other formats are not supported by the portal.
- The instruction slide itself may be deleted after the idea content is added.

The uploaded creator-notes file also recommends explaining technology choices, pairing risks with mitigations, showing the actual process, including relevant research, and preparing a concise pitch. Those notes describe the creator’s advice, not additional official template rules.

## Project summary for the deck

### Problem

Ambedkar’s writings, speeches, Constituent Assembly debates, manuscripts, and historical records are held across separate repositories and formats. The project brief identifies fragmented access, limited intelligent search, and the need for multilingual and interactive access for students, researchers, institutional visitors, and the public.

### Proposed solution

Build an institutional digital archive that collects and standardizes records, preserves full text and metadata, and lets visitors search, filter, read, and explore records through an accessible web/kiosk-mode interface. A backend API provides archive functions. An OCR-assisted contribution flow can extract text for staff review before ingestion. Cited research retrieval, timeline browsing, and speech narration are included in the prototype/source code.

### Innovation to describe accurately

- Combines records from Internet Archive, Constituent Assembly Debates, and Dr. Ambedkar Foundation/BAWS sources in a common document schema.
- Connects full-text search and cited records with an interactive archive, timeline, and research interface.
- Includes an OCR review-and-ingest path and a kiosk-mode interface.
- Uses archive-grounded retrieval to expose relevant source records. **Do not call the current search semantic/vector search or claim a generative AI model unless a deployed implementation is verified.**

## Dataset inventory

The project’s inventory report and registry were generated on **25 September 2026** and report this baseline:

| Baseline measure | Reported value |
|---|---:|
| Records | **530** |
| Indexed words | **86,624** |
| Embedding-ready text chunks | **835** |
| Internet Archive records | **510** |
| Constituent Assembly Debates (CAD) records | **10** |
| Foundation / BAWS records | **10** |

The baseline record types are 423 publications, 63 speeches, 20 debates, 20 other records, and 4 manuscripts. The baseline language distribution is English 410, Hindi 42, Telugu 27, Marathi 18, Bengali 11, Gujarati 9, Tamil 9, Punjabi 2, Malayalam 1, and Kannada 1. These are **record languages in the archive inventory**, not proof that the complete interface or every document is translated into all ten languages.

### Important count mismatch: reconcile before claiming a live total

The files currently in the working repository do not all reflect the same dataset snapshot:

- `data_inventory_report.json`, `registry.json`, and `combined_metadata.csv` still report **530** baseline records.
- The `processed_data` folder currently contains **532** JSON files. Two additions are `DOC_MANUAL_1790693685770` and `DOC_TEST_001`.
- The current SQLite database contains **531** document rows and 531 FTS5 rows. It includes the manual record but not `DOC_TEST_001`.
- The chunk table contains **835** rows.
- The current working folder’s total record word-count field sums to 86,818, while the dated inventory reports 86,624.
- The inventory/registry contains an old absolute database path under `C:\Users\Vihal\Downloads\New folder\...`; application code configures the database relative to this project.

**Presentation guidance:** If a number is needed, label 530 as the **reported baseline inventory (25 Sep 2026)**. Do not say that the live database currently has 530 rows. Mention the repository/database reconciliation as a pre-deployment task or presenter note; do not turn the conflicting counts into a claimed performance metric.

### Dataset files and document schema

Main data locations:

- `ambedkar_archive_data/raw_documents/ia_raw_records.json` — raw Internet Archive source records.
- `ambedkar_archive_data/raw_documents/cad_raw_records.json` — raw Constituent Assembly Debate records.
- `ambedkar_archive_data/raw_documents/foundation_raw_records.json` — raw Foundation/BAWS records.
- `ambedkar_archive_data/processed_data/` — one normalized JSON wrapper per processed document.
- `ambedkar_archive_data/metadata/registry.json` — baseline record registry.
- `ambedkar_archive_data/metadata/combined_metadata.csv` — baseline tabular metadata export.
- `ambedkar_archive_data/metadata/data_inventory_report.json` — dated inventory snapshot.
- `ambedkar_archive_data/texts/` — extracted text files for selected works.

Each processed JSON record follows a `document` object containing an ID, title, author, date, type, language, content (`full_text`, `summary`, `key_quotes`), metadata (source, archive reference, collection, pages/word count where present), tags, relationships, optional translations, and media references.

The project’s `images/` and `audio_video/` archive directories are empty in the reviewed checkout. The web page has a separate Ambedkar portrait asset. Do not imply that a complete local audio/video collection has already been loaded.

## Database and search design

**Database:** SQLite at `ambedkar_archive_data/database/ambedkar_archive.db` (about 5.8 MB in the reviewed checkout).

| Table | Role |
|---|---|
| `documents` | Structured record fields, full text, metadata, translations/media JSON, and raw JSON |
| `documents_fts` | SQLite FTS5 index over title, summary, full text, and tags |
| `chunks_for_embeddings` | Overlapping text chunks prepared for a possible embedding/vector-search stage |

The ingestion script splits text into chunks of up to 250 words with 50-word overlap. The database contains 835 chunk rows, but the repository does **not** implement a live vector index or embedding model. The current search code uses SQLite FTS5 keyword/prefix matching; the research assistant retrieves matching archive passages and attaches citations. Do not describe this as semantic/vector search or claim a general-purpose LLM is deployed.

The pipeline code collects records, normalizes them to a common schema, validates required fields, then writes processed JSON, a registry, CSV metadata, SQLite documents, an FTS5 index, and chunks. The project includes schema validation code; the 100% validation statement in the old README/report applies to its 530-record baseline and has not been re-established for the two extra current JSON files.

## Current software and implementation status

| Component | Present in project | Safe deck claim / caveat |
|---|---|---|
| Frontend | HTML, CSS, vanilla JavaScript; Tailwind CSS and Font Awesome load from CDNs | Web archive prototype with Archive, Timeline, Research, About, and Contribute sections; English/Hindi/Marathi interface controls; light/dark theme; kiosk/full-screen mode |
| Backend | Python FastAPI in `backend/app.py` | API source includes search, statistics, document listing/detail, timeline, OCR, ingestion, exports, research retrieval, and TTS routes. Say “implemented in backend code” unless the API is actually running and demonstrated. |
| Preview server | Node.js `frontend/preview-server.js` | Current local preview serves the frontend, processed document details, and an archive-wide research endpoint. It returns unavailable responses for other `/api/*` routes; do not present preview mode as the full API deployment. |
| Search | SQLite FTS5 in backend; keyword scoring over processed JSON in preview | Full-text/keyword archive search with filters and source records. Semantic/vector retrieval remains future work. |
| Research assistant | Archive passage retrieval, localized interface copy, citations/excerpts | Describe as a prototype archive research assistant grounded in indexed records; avoid “zero hallucination,” autonomous reasoning, or deployed LLM claims. |
| OCR | PyMuPDF, Pillow, pytesseract/Tesseract code path | PDF/image extraction is available when Tesseract and the requested language pack are installed. Upload is limited to 20 MB and PDFs to 50 pages. Staff should review OCR text before ingestion. |
| Audio | Browser SpeechSynthesis fallback; optional ElevenLabs TTS API in backend | Narration is available as a feature path. ElevenLabs requires configured credentials and access. Do not promise a complete prerecorded audio archive. |
| Translation/languages | Ten source-language codes in the baseline corpus; EN/HI/MR UI; Hindi and Marathi translation fields | Explain corpus language coverage separately from interface language and verified translation coverage. Do not claim every record is fully translated or narrated in ten languages. |
| Physical devices | No hardware model or physical kiosk deployment in the reviewed repository | Kiosk mode exists in the website. Touchscreen kiosks, smart displays, audio-visual playback equipment, and institutional server hardware are proposed deployment hardware, not verified installed devices. |

### Current architecture flow

```text
Internet Archive + CAD + Foundation/BAWS
        ↓
Collectors → normalize to common schema → validate → OCR/review when needed
        ↓
Processed JSON + metadata registry/CSV + SQLite documents + FTS5 + chunk table
        ↓
FastAPI archive services (full backend code) / Node preview (partial runtime)
        ↓
Web archive → browse/search/read → timeline/research/citations → narration
        ↓
Visitors and researchers now; physical kiosks/displays after institutional deployment
```

### Version language for the presentation

No formal release tags are present in the reviewed project, so treat these as **project stages**, not published software version numbers:

- **V0 — Problem definition:** fragmented source collections and limited unified access.
- **V1 — Current prototype:** normalized corpus, SQLite/FTS5, web interface, API source, timeline, OCR path, archive retrieval, narration options. The local preview exposes only part of the API; dataset counts need reconciliation.
- **V2 — Institutional pilot (proposed):** run and verify the full backend/database on institutional infrastructure; connect and test real touchscreen kiosks, smart displays, and audio-visual equipment; establish admin access, backups, and operational support.
- **V3 — Multilingual intelligence (proposed):** implement and evaluate live semantic/vector retrieval; verify document translations and language-specific answers/narration.
- **V4 — Preservation at scale (proposed):** redundant copies, monitoring, audit and recovery procedures, and governed cooperation across institutions.

Clearly label V2–V4 **planned**. The user interface’s kiosk mode is not the same as a deployed kiosk. The chunk table is not the same as live vector search.

## Hardware extracted from the project brief

The brief explicitly proposes:

- Interactive touchscreen kiosks.
- Smart displays.
- Centralized archival/institutional servers.
- Audio-visual systems for archive playback.

The repository does not state hardware models, quantities, specifications, procurement cost, or a completed installation. Do not invent any. Treat the list as proposed SIH hardware and explain what each device enables. Possible operational cost categories include devices, server/storage/backup, installation, digitization, connectivity, and support, but no project estimate is available.

## Feasibility, viability, risks, and mitigation content

### Feasibility evidence

- **Technical:** A 530-record baseline, standardized JSON, SQLite/FTS5, ETL/schema-validation code, web UI, API source, and OCR/TTS paths provide a prototype foundation.
- **Financial:** No budget, vendor quote, hosting estimate, or API-cost estimate is in the project files. Present cost categories only and request institutional/vendor estimates.
- **Market/user need:** The brief names students, researchers, institutional visitors, archivists, and the general public. No survey, adoption result, or market sizing is provided.
- **Operational:** An institutional archive needs source/rights review, metadata review, OCR proofreading, data stewardship, backup/recovery, device support, and a responsible ingestion workflow. These are deployment requirements, not completed project features.

### Risks and credible responses

| Risk | Mitigation to present as a plan |
|---|---|
| Inventory, registry, CSV, and database are out of sync | Reconcile IDs and counts; exclude test records from production; regenerate registry/CSV/report; rerun validation before deployment |
| OCR may misread scans | Keep a human correction step, preserve the source scan/reference, and track corrected text quality |
| Search assistant can return weak or unrelated passages | Test a question set against archive records, show exact citations, use “not found in archive” behavior, and evaluate relevance before adding semantic retrieval |
| Ten source languages do not mean full UI/translation coverage | Verify each language’s actual content and translation quality; add one language at a time with human review |
| OCR and TTS depend on installed/configured components | Package and test Tesseract language data; provide browser speech fallback; budget and protect any external TTS credentials |
| Current UI loads Tailwind and Font Awesome from CDNs | Vendor/static-host assets for a controlled offline institutional deployment and test without internet access |
| Physical hardware is not yet integrated | Pilot a specific kiosk/display setup and test accessibility, audio, connectivity, heat/power, and staff support before rollout |
| Archival permissions and provenance | Confirm rights/access terms for each source, preserve attribution, and have institutional archivists approve ingest policy |

## Impact and benefits

State these as expected benefits, not measured outcomes:

- Easier discovery of Ambedkar’s writings, speeches, constitutional debates, and historical records.
- Broader access for students, researchers, visitors, and the public through web and proposed institutional kiosks.
- More consistent preservation through metadata, normalized records, searchable text, and planned backup procedures.
- More accessible learning through a timeline, readable summaries, narration, and a multilingual interface.
- Support for constitutional awareness and archival research.

No visitor counts, learning gains, digitization-cost savings, or economic-impact measurements are in the reviewed project files. If the slide uses metrics, label them as **pilot KPIs/targets**, not achieved results. Suggested future measures: successful search rate, time to locate a cited record, OCR correction rate, kiosk task completion, language-specific use, and archive availability.

## Research and references slide: verified project records to cite

Use concise primary-source citations taken from the normalized archive. Preserve volume/page information and do not manufacture URLs where the record has none.

1. **B. R. Ambedkar, _Annihilation of Caste_**, Dr. Babasaheb Ambedkar Writings and Speeches, Vol. 1, pp. 23–96. Archive record ID `DOC_DAF_BAWS_PUB_1936_AOC`; archive reference `DAF-BAWS_PUB_1936_AOC`.
2. **B. R. Ambedkar, Constituent Assembly of India Debates**, Vol. XI, pp. 972–984, speech commonly associated with “Grammar of Anarchy.” Archive record ID `DOC_CAD_CAD_VOL11_19491125`; archive reference `CAD-LS-Volume XI-972-984`. The record’s translation metadata lists `https://www.loksabha.gov.in/DisplayCAD`; verify the destination before placing it on the slide.
3. **B. R. Ambedkar, _The Problem of the Rupee: Its Origin and Its Solution_**, BAWS Vol. 6, pp. 315–620. Archive record ID `DOC_DAF_BAWS_PUB_1923_POR`; archive reference `DAF-BAWS_PUB_1923_POR`.
4. **B. R. Ambedkar, _Waiting for a Visa: Autobiographical Life Sketches_**, BAWS Vol. 12, pp. 661–691. Archive record ID `DOC_DAF_BAWS_PUB_1935_WFV`; archive reference `DAF-BAWS_PUB_1935_WFV`.

The reference slide can cite the SIH problem source and the project’s source repositories as well. Add only research papers or external sources actually checked by the team. Keep citations small but readable; if the official template has no room for full URLs, use short citations on-slide and place the verified links in a speaker note or accompanying project material if permitted.

## Recommended content by template slide

### Slide 1 — Title page

- Project title: **Dr. B. R. Ambedkar Digital Heritage Archive**.
- Problem Statement ID: **26096**.
- Theme: **Smart Education**.
- PS category: **Hardware (with Integrated Software)**.
- Official PS title, team ID, and registered team name: fill from SIH portal; never guess.

### Slide 2 — Proposed Solution

Use a short problem statement and solution, then one line on what the prototype demonstrates. Explain the combined searchable archive, standardized records, cited retrieval, timeline, and accessible visitor interface. Distinguish the existing web/kiosk-mode prototype from future physical installations. State the archive’s integrated primary-source collection as the project’s differentiator without claiming it is the first or only platform.

### Slide 3 — Technical Approach

Show a simple, editable, left-to-right workflow from repositories through collection, normalization/validation/OCR review, JSON/SQLite/FTS5, API/search/retrieval, web interface, and visitor/device access. Pair each technology with its role: Python/FastAPI for APIs, SQLite/FTS5 for local structured full-text retrieval, HTML/CSS/JavaScript for the interface, Tesseract for optional OCR, and browser speech/optional ElevenLabs for narration. Mark live vector search and physical kiosk deployment as planned, not current.

### Slide 4 — Feasibility and Viability

Cover technical, financial, market/user, and operational feasibility. Use project evidence above. Include two to four meaningful risks with mitigations, especially data reconciliation, OCR quality, multilingual verification, offline packaging, and hardware pilot. State that cost estimates and user research remain to be completed; do not make up rupee values.

### Slide 5 — Impact and Benefits

Connect expected benefits to students, researchers, archivists, institutional visitors, and the public. Use outcomes such as easier access, preservation, multilingual learning, and constitutional awareness. Do not present targets as achieved results or create fabricated impact charts.

### Slide 6 — Research and References

Use short citations for the selected primary records listed above and any independently verified technical/research references added by the team. Ensure every citation corresponds to a real item and avoid fabricated authors, titles, journals, dates, or links.

## Copy-ready master prompt for Canva AI

Upload these three files to Canva: (1) `SIH2026-IDEA-Presentation-Format.pptx`, (2) `sih_2026_ppt_layout_and_creator_notes.md`, and (3) this Markdown file. Then give Canva AI the prompt below.

```text
Create the SIH 2026 idea presentation in Canva using the uploaded SIH PowerPoint template as the actual starting design. Use the uploaded layout/creator notes and the project brief as reference material.

SOURCE PRIORITY
1. Follow the uploaded PowerPoint template for official slide headings, required idea-detail pointers, layout, and submission rules.
2. Use the project brief Markdown as the source of project facts and dataset/database details.
3. Treat the creator-notes Markdown as secondary presentation advice. It must not override the PowerPoint template.

TEMPLATE AND OUTPUT RULES
- Keep the template’s 16:9 size, SIH logo, blue footer, slide-number treatment, visual theme, required fields, and idea-detail pointers. Fill the template rather than redesigning it.
- The final submission must contain no more than six slides including the title slide. Use the first six content slides and delete the template’s seventh “Important Instructions” slide after applying its rules.
- Do not add a cover, appendix, agenda, thank-you, or other extra slide.
- Keep the Canva design editable for the team. Export the final submission as PDF because the supplied template says the SIH portal accepts PDF only. Do not claim that the Canva/PPT file is the submission format.
- Use concise text and a simple, readable workflow diagram. Preserve all required template headings and fields.

FACT AND STATUS RULES
- Use only facts in the project brief and uploaded files. Never invent the official PS title, team ID/name, costs, hardware models, partners, deployment, citations, user research, measured impact, performance, or language/translation coverage.
- Put [FILL FROM SIH PORTAL] in any missing team/title fields rather than guessing.
- Label the 530-record, 86,624-word, 835-chunk figures as the reported baseline inventory dated 25 September 2026. Do not claim the current working database has 530 rows: the project files are out of sync. Mention reconciliation as a deployment task or presenter note.
- Describe current search as SQLite FTS5/keyword retrieval with cited archive records. The chunk table is embedding-ready, but live vector/semantic search is not implemented.
- Describe the research assistant as an archive-grounded retrieval prototype. Do not claim a deployed general-purpose LLM or “zero hallucination.”
- Separate ten source languages in the baseline corpus from the English/Hindi/Marathi interface controls. Do not claim every source is fully translated or narrated in ten languages.
- Kiosk mode exists in the web interface. Physical touchscreen kiosks, smart displays, audio-visual equipment, and institutional server deployment are proposed, not verified installations.
- The full FastAPI backend exists in source code. The current Node preview exposes only part of the API. Do not imply all backend services are running in the current preview.
- No cost estimates or measured impact are in the files. Use cost categories and suggested future pilot KPIs only when clearly marked as estimates to be gathered or targets, never as results.
- Use real archival citations listed in the project brief. Do not fabricate references or URLs.

SLIDE CONTENT
Slide 1, Title page: Dr. B. R. Ambedkar Digital Heritage Archive; Problem Statement ID 26096; Theme Smart Education; Category Hardware (with Integrated Software); placeholders for the exact official PS title, team ID, and registered team name.

Slide 2, Proposed Solution: explain the fragmented-access problem and the searchable institutional archive solution. Show how normalized primary-source records, cited retrieval, timeline exploration, and accessible visitor access address it. State the project’s integration of three source groups as its differentiator without unsupported “first/only” claims.

Slide 3, Technical Approach: create a simple editable flow diagram:
Internet Archive + Constituent Assembly Debates + Foundation/BAWS
→ collectors and document intake
→ schema normalization, validation, optional OCR and human review
→ processed JSON + metadata registry/CSV + SQLite documents + FTS5 index
→ FastAPI archive services and archive-grounded cited retrieval
→ web archive: browse/search/read, timeline, research, narration
→ current browser users and proposed institutional kiosk/display hardware.
Label Python/FastAPI, SQLite FTS5, HTML/CSS/JavaScript, optional Tesseract OCR, and browser/optional ElevenLabs narration by their role. Add a small, clearly marked “Planned” tag for live vector search and physical kiosk deployment. Do not imply that embedding-ready chunks already power semantic retrieval.

Slide 4, Feasibility and Viability: show technical readiness from the existing corpus, database, pipeline, interface, and API source. Cover financial, market/user, and operational questions honestly. Show key risks with practical mitigations: reconcile the records/database, review OCR, verify translations, package CDN assets for offline use, and pilot hardware. State that costs and user research are still to be gathered.

Slide 5, Impact and Benefits: connect expected benefits to students, researchers, archivists, institutional visitors, and the public. Focus on discovery, preservation, accessible learning, and constitutional awareness. Use no fabricated results or impact numbers.

Slide 6, Research and References: cite real primary archive records with short volume/page references: Annihilation of Caste (BAWS Vol. 1, pp. 23–96); Constituent Assembly Debates (Vol. XI, pp. 972–984); The Problem of the Rupee (BAWS Vol. 6, pp. 315–620); and Waiting for a Visa (BAWS Vol. 12, pp. 661–691). Use verified links only; the project brief supplies archive IDs and the Lok Sabha CAD URL for checking.

FINAL QUALITY CHECK
Check the result against the supplied template: six slides maximum, correct order, required titles/fields preserved, readable text, accurate current-versus-planned labels, no invented claims, citations traceable to real records, and PDF export ready for the SIH portal. Keep explanations understandable to both technical and non-technical evaluators.
```
