"""
Pydantic Data Models for Ambedkar Digital Heritage Archive API
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class ContentModel(BaseModel):
    full_text: str = ""
    summary: str = ""
    key_quotes: List[str] = []

class MetadataModel(BaseModel):
    source: str = "IA"
    archive_reference: str = ""
    collection: str = ""
    pages: int = 1
    word_count: int = 0
    condition: str = "good"
    accessibility: str = "public"
    downloads: Optional[int] = 0
    url: Optional[str] = ""
    pdf_url: Optional[str] = ""

class DocumentItem(BaseModel):
    id: str
    title: str
    author: str = "Dr. B.R. Ambedkar"
    date: Optional[str] = None
    type: str = "publication"
    language: str = "en"
    content: ContentModel
    metadata: MetadataModel
    tags: List[str] = []
    relations: Dict[str, Any] = {}
    translations: Dict[str, Any] = {}
    media: Dict[str, Any] = {}

class DocumentWrapper(BaseModel):
    document: DocumentItem

class SearchQuery(BaseModel):
    q: str
    language: Optional[str] = None
    document_type: Optional[str] = None
    source: Optional[str] = None
    limit: int = Field(default=20, ge=1, le=100)
    offset: int = Field(default=0, ge=0)

class SearchResultItem(BaseModel):
    id: str
    title: str
    author: str
    date: Optional[str]
    type: str
    language: str
    source: str
    summary: str
    tags: List[str]
    url: Optional[str] = None

class SearchResponse(BaseModel):
    query: str
    total: int
    took_ms: float
    results: List[SearchResultItem]

class StatsResponse(BaseModel):
    total_documents: int
    total_words_indexed: int
    total_embedding_chunks: int
    languages: Dict[str, int]
    languages_by_source: Dict[str, Dict[str, int]] = Field(default_factory=dict)
    types: Dict[str, int]
    sources: Dict[str, int]
