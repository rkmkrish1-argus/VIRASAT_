# Requirements: Dr. B. R. Ambedkar Digital Heritage Archive

**Project:** AI-powered institutional archive and audio-visual knowledge platform  
**Intended institution:** Dr. Ambedkar International Centre (DAIC) and partner institutions  
**Status:** Requirements and staged implementation plan  
**Purpose:** Define the target system and record current model/AI progress without presenting planned capabilities as already deployed.

## 1. Vision

Develop a centralized, hardware-and-software-integrated digital archive that preserves and opens access to Dr. B. R. Ambedkar's writings, speeches, historical records, and constitutional ideas. Researchers, students, institutional visitors, and the general public should be able to discover, study, listen to, and compile trusted archival material through accessible web experiences, interactive kiosks, and smart displays.

The platform should promote digital preservation, constitutional awareness, accessible learning, and immersive heritage experiences. Search and AI answers must be grounded in identifiable archival sources, with provenance and citations visible to users.

## 2. Scope

The target solution includes:

- A centralized archive catalog, document store, metadata registry, and institutional administration tools.
- A visitor-facing web interface that can run in kiosk mode, plus deployment support for interactive kiosks and smart displays.
- Search, browse, read, listen, and research workflows over writings, speeches, debates, manuscripts, photographs, and audio-video records.
- OCR-assisted digitization, staff review, and controlled ingestion of authorized materials.
- Multilingual access, translation, and narration capabilities, with language coverage stated per document and feature.
- Preservation, access control, backups, auditability, and export/interoperability functions for institutional use.

This document describes the desired system as well as the repository's current implementation baseline. Items described as planned require implementation, evaluation, and institutional deployment before they can be claimed as operational.

## 3. Users and permissions

| User | Main needs |
|---|---|
| Visitor / general public | Find, read, listen to, and explore public archival records using an accessible interface. |
| Student / educator | Discover materials by topic, date, language, and type; use timelines and curated learning paths. |
| Researcher | Search full text, inspect source records and citations, compare documents, and compile references. |
| Archivist / content editor | Review metadata and OCR, correct records, manage rights and publication status, and ingest authorized content. |
| Institutional administrator | Manage users, collections, devices, preservation policies, integrations, monitoring, and audit records. |

Public users should only access material approved for public release. Editing, ingestion, administration, and restricted collection access must require authenticated roles.

## 4. Functional requirements

### 4.1 Archive discovery and document access

- **FR-01:** Provide full-text search across indexed titles, summaries, text, and tags.
- **FR-02:** Provide filters for language, document type, date, collection, and source, with pagination and clear result counts.
- **FR-03:** Support semantic search and intelligent knowledge mapping so users can discover conceptually related records, people, events, and constitutional themes.
- **FR-04:** Show a document detail view with available full text, summary, metadata, source/provenance, rights/access status, related records, and supported media.
- **FR-05:** Allow users to save or compile selected records into a reading/research list and export references where permitted.
- **FR-06:** Clearly distinguish a full transcription from a summary, OCR extraction, translation, or catalog description.

### 4.2 OCR and digitization

- **FR-07:** Accept authorized scanned documents and images for OCR processing, including applicable manuscript and historical-document workflows.
- **FR-08:** Detect or let staff select the source language and record OCR engine, language pack, processing date, and confidence/quality information when available.
- **FR-09:** Present extracted text for human correction and approval before it becomes searchable or publicly visible.
- **FR-10:** Preserve links between the digital object, page/image sequence, extracted text, corrected transcript, and source metadata.
- **FR-11:** Retain an original preservation master and create separate access derivatives; do not overwrite the original file during OCR or normalization.

### 4.3 Multilingual access and narration

- **FR-12:** Support multilingual metadata and user-interface labels, and provide translations for selected archival content.
- **FR-13:** Label translation language, method, review status, and relationship to the source text. Machine translation must not be presented as a verified human translation.
- **FR-14:** Provide audio narration for eligible full text and summaries, including language and voice selection when available.
- **FR-15:** Provide text alternatives and playback controls, and indicate when audio is generated on demand versus an archival recording.

### 4.4 Audio-video archive

- **FR-16:** Catalog lectures, documentaries, interviews, speeches, and other approved audio-video material.
- **FR-17:** Store descriptive metadata, rights, source/provenance, duration, language, captions/transcripts, and stable media references.
- **FR-18:** Support accessible playback, captions/transcripts where available, and links between recordings and related people, works, events, or timeline entries.
- **FR-19:** Distinguish digitized archival recordings from newly generated narration and other derivative media.

### 4.5 Timeline and heritage storytelling

- **FR-20:** Provide an interactive, source-linked timeline of significant life, work, and constitutional milestones.
- **FR-21:** Provide curated memorial and storytelling modules that connect narrative segments to original records and explain the evidence behind dates and claims.
- **FR-22:** Allow editors to manage timeline entries and stories through a reviewable content workflow.

### 4.6 AI research assistant

- **FR-23:** Answer questions about Dr. Ambedkar's works and constitutional ideas using retrieval over approved archive content.
- **FR-24:** Cite the source documents and passages supporting each answer and provide direct navigation to those records.
- **FR-25:** State when the archive does not contain enough evidence to answer; do not invent quotations, references, dates, or claims.
- **FR-26:** Keep generated answers separate from archival source text and label them as AI-generated explanations.
- **FR-27:** Apply language-aware retrieval and provide a clear indication when translated material or cross-language retrieval was used.
- **FR-28:** Maintain an evaluation set covering factual questions, source attribution, unanswerable questions, and relevant languages; review failures before expanding deployment.

### 4.7 Preservation and institutional management

- **FR-29:** Maintain structured, searchable metadata and stable identifiers for records, digital objects, and derivatives.
- **FR-30:** Record source, custody/provenance, rights and access conditions, digitization history, and editorial changes.
- **FR-31:** Provide secure staff authentication, role-based permissions, audit logs, and controlled publication workflows.
- **FR-32:** Support integrity checks, backup and recovery, preservation copies, and documented retention procedures.
- **FR-33:** Support institutional metadata export and authorized integration with partner repositories and catalogs.
- **FR-34:** Report ingestion and preservation health, including failures, incomplete metadata, and records awaiting review.

### 4.8 Kiosks and smart displays

- **FR-35:** Provide a touch-friendly, accessible visitor experience suitable for full-screen kiosk use.
- **FR-36:** Support deployment on institutional kiosks and smart displays, with device configuration, session reset, and content update procedures.
- **FR-37:** Provide visitor controls for search, reading, listening, timeline exploration, and compiling a temporary collection.
- **FR-38:** Clear session-specific selections and personal data after a kiosk session ends.

## 5. Non-functional requirements

- **NFR-01 Accessibility:** Follow applicable accessibility standards, including keyboard/touch navigation, readable contrast, scalable text, captions, and screen-reader-friendly structure.
- **NFR-02 Performance:** Make common catalog and full-text searches responsive under the expected institutional load; measure and publish performance using repeatable conditions.
- **NFR-03 Reliability:** Provide monitored services, recoverable backups, and documented recovery objectives appropriate to the institution.
- **NFR-04 Security:** Use secure transport, least-privilege access, protected secrets, input validation, and security updates. Do not embed service credentials in frontend code.
- **NFR-05 Privacy:** Minimize collection of visitor data, explain any retained data, and apply institutional retention and consent policies.
- **NFR-06 Interoperability:** Use documented schemas, stable identifiers, and export formats that support migration and partner exchange.
- **NFR-07 Provenance:** Keep source and transformation information attached to records and derived text/media throughout ingestion and display.
- **NFR-08 Resilience:** Core browsing and search should be deployable on institution-controlled infrastructure; define which functions require external services and what remains available without them.
- **NFR-09 Maintainability:** Document configuration, deployment, backups, ingestion, model versions, and operational procedures.
- **NFR-10 Rights compliance:** Ingest, preserve, transform, and display content according to applicable permissions, licenses, and institutional agreements.

## 6. Model and AI progress

This section describes a staged path from the current code baseline to the requested intelligent archive. A capability is considered complete only when implemented, tested on representative archival data, and documented with its limitations.

### Current baseline in this repository

- A normalized archive corpus and metadata schema are present. The project brief reports a 530-record baseline snapshot; repository and database counts have been observed to differ, so counts must be reconciled before being stated as a current total.
- SQLite FTS5 provides keyword/full-text search. The project includes text chunks prepared for a possible embedding stage, but these chunks do **not** constitute a live vector index or deployed embedding model.
- The research-assistant path retrieves matching archive passages and returns citations. It should be described as archive-grounded retrieval, not as a verified generative model or guaranteed hallucination-free system.
- OCR code paths support PDF/image extraction when required OCR software and language data are installed. Human review remains necessary before ingestion.
- Narration code paths include browser speech synthesis and an optional configured text-to-speech provider. Availability depends on runtime configuration and provider access.
- The interface includes timeline and kiosk-mode experiences. Physical kiosks, smart displays, a complete local audio-video archive, and institution-wide preservation operations remain deployment goals unless separately verified.

### Model capability stages

| Stage | Capability and deliverable | Completion evidence |
|---|---|---|
| **M0 — Current prototype** | Keyword retrieval, archive passage lookup with citations, OCR-assisted extraction, and optional speech synthesis paths. | Demonstrate against the current corpus; reconcile dataset/database counts; document enabled versus configuration-dependent features. |
| **M1 — Semantic retrieval** | Add an embedding model and vector index for semantic search; combine with keyword retrieval and metadata filters. | Retrieval evaluation on curated queries, including names, concepts, historical terminology, multilingual queries, and precision/source relevance review. |
| **M2 — Knowledge mapping** | Extract or curate relationships among works, people, institutions, events, dates, and constitutional concepts; expose navigable, source-linked connections. | Every displayed relationship has provenance and editorial/model confidence; archivists review quality and false links. |
| **M3 — OCR quality workflow** | Improve OCR for historical print and manuscripts, with language-specific processing, page alignment, and confidence-assisted correction. | Character/word accuracy measured on representative, manually transcribed samples by script and document condition; approval workflow demonstrated. |
| **M4 — Translation and multilingual narration** | Add translation workflows and language-aware narration for selected content. | Translation coverage and review status shown per item; quality reviewed by qualified speakers; narration checked for language, pronunciation, and accessibility. |
| **M5 — Grounded research assistant** | Add or integrate a language model to formulate answers from retrieved primary sources, with passage citations and abstention. | Evaluation for factuality, citation support, unsupported-answer refusal, and language coverage; human review of failures and clear AI labeling. |
| **M6 — Audio-video intelligence** | Add transcripts/captions and search over approved recordings; connect media to the archive and timeline. | Rights-reviewed test collection, transcript accuracy checks, synchronized playback/captions, and source-linked search results. |
| **M7 — Institutional deployment** | Operate the integrated archive on institutional infrastructure with kiosks/displays, preservation controls, administrative workflows, and monitoring. | DAIC or partner pilot acceptance, security and recovery review, accessibility checks, device testing, and documented operations. |

Stages may overlap where dependencies allow, but model selection, language coverage, and acceptance thresholds must be recorded before a stage is declared complete. The archive should retain original source material and make model-generated or machine-transformed content identifiable and reviewable.

## 7. Acceptance criteria

The target solution is acceptable when:

1. Visitors can find, open, and cite or save relevant records through accessible web and kiosk interfaces.
2. Full-text and semantic search return relevant records with filters and visible provenance.
3. Staff can digitize authorized items, review OCR output, correct metadata/text, and publish through role-based workflows.
4. Supported translations and narrations identify their language and review/generation status.
5. Audio-video records, timeline entries, and memorial stories link back to the relevant archival sources.
6. The research assistant provides evidence-linked answers, cites passages, and declines questions unsupported by the indexed archive.
7. Preservation copies, integrity checks, backups, audit records, and recovery procedures are operational and demonstrated.
8. Hardware deployment on interactive kiosks and smart displays is tested at the intended institution.
9. Claims about corpus size, language coverage, model capability, performance, and hardware deployment are supported by current verification data.

## 8. Dependencies and open implementation decisions

- Institutional authorization, copyright/rights review, and agreements for content and partner-repository access.
- Hardware and network specifications for kiosks, smart displays, storage, and institutional hosting.
- Model and service selection for embeddings, language generation, OCR, translation, speech, and media transcription, including offline requirements and data-governance constraints.
- Language priorities and qualified reviewers for translation, OCR, narration, and answer evaluation.
- Preservation policy, metadata standard, backup location, retention period, and recovery objectives.
- Reconciliation of dataset inventory, processed files, and live database before publishing operational counts.

## 9. Source of current-state statements

Current implementation notes in this document are summarized from the repository `README.md` and `SIH2026_PPT_Content_Brief_and_Canva_Prompt.md`. The presentation brief records important qualifications about data-count discrepancies, FTS5 versus vector search, preview versus full API behavior, translation coverage, and physical hardware deployment. Revalidate those statements against the running system before a production release or external presentation.
