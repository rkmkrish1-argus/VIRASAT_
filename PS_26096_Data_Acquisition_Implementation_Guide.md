# PS 26096: DATA ACQUISITION & IMPLEMENTATION GUIDE

## Digital Heritage Archive for Dr. B.R. Ambedkar
### Complete Roadmap for Data Collection and Development

---

## PART 1: DATA ACQUISITION STRATEGY

### 1.1 Data Sources & Collection Priorities

#### **TIER 1: CRITICAL DATA SOURCES** (Start Here First)

##### A. Dr. Ambedkar Foundation (DAF)
**Location:** New Delhi  
**Contact:** [https://www.ambedkarfoundation.org](https://www.ambedkarfoundation.org)

**What They Have:**
- Primary documents collection (~10,000-20,000 items)
- Original manuscripts and letters
- Photographs and archival materials
- Publications and writings

**How to Access:**
```
Direct Contact:
- Email: foundation@ambedkarfoundation.org
- Phone: +91-11-XXXX-XXXX (verify on website)

Request Process:
1. Write formal letter/email requesting data access
2. Mention SIH participation (government legitimacy)
3. Ask for:
   - High-res scans of key documents
   - Metadata (titles, dates, descriptions)
   - Permission for digitization
   - Bulk export rights (CSV/JSON of metadata)

Timeline: 1-2 weeks for initial response
```

**Data Format to Request:**
```json
{
  "document_id": "DAF_001",
  "title": "Document Title",
  "author": "Dr. B.R. Ambedkar",
  "date": "YYYY-MM-DD",
  "type": "manuscript|letter|speech|publication",
  "language": "en|hi|mr|ta|te|ka|bn",
  "tags": ["constitutional", "social_justice"],
  "file_url": "path_to_scan.pdf",
  "metadata": {
    "pages": 15,
    "condition": "good|fair|poor",
    "archival_reference": "DAF_MS_123"
  }
}
```

---

##### B. Constituent Assembly Debates Archive (Lok Sabha)
**Location:** Parliament of India, New Delhi  
**URL:** [https://www.loksabha.gov.in/DisplayCAD](https://www.loksabha.gov.in/DisplayCAD)

**What They Have:**
- Complete Constitutional Assembly Debates (1946-1949)
- ~7,500+ pages of debates
- Ambedkar's speeches and interventions
- Already partially digitized

**How to Access:**
```
PUBLIC ACCESS:
1. Website already has digitized debates (free)
2. Download CAD PDFs directly
3. Extract structured data using tools below

API/Bulk Access:
- Contact: Lok Sabha Library & Reference Section
- Email: library@loksabha.gov.in
- Request: Bulk export of CAD in structured format
```

**Sample Data from CAD:**
```
Date: November 26, 1949
Speaker: Dr. B.R. Ambedkar
Topic: Preamble to the Constitution
Content: "India is a federal union. But the federal union..."
Page: 456
Volume: 5
Language: English
```

---

##### C. National Digital Library of India (NDL)
**URL:** [https://www.ndl.iitkgp.ac.in](https://www.ndl.iitkgp.ac.in)

**What They Have:**
- 200M+ digital objects (books, journals, theses)
- Ambedkar-related materials scattered
- Open API for searching and downloading

**How to Access:**
```
AUTOMATED API ACCESS:

1. Search Endpoint:
   https://www.ndl.iitkgp.ac.in/api/search?
   q=Ambedkar&
   rpp=100&
   page=1

2. Python Script (see below):
   - Query all Ambedkar materials
   - Bulk download metadata
   - Extract relevant items

3. Documentation:
   https://www.ndl.iitkgp.ac.in/page/developers

Key Search Queries:
- "Dr. Ambedkar"
- "B.R. Ambedkar"
- "Constitutional Assembly Debates"
- "Annihilation of Caste"
- "The Buddha and His Dhamma"
```

---

##### D. Columbia University Library
**URL:** [https://library.columbia.edu](https://library.columbia.edu)

**What They Have:**
- Ambedkar's personal papers from his time as student
- Correspondence and study materials
- International perspective materials

**How to Access:**
```
REMOTE ACCESS:

1. Create Account:
   - Visit Columbia Libraries website
   - Register as international researcher
   - May require institutional affiliation

2. Request Materials:
   - Online finding aids available
   - Can scan materials for academic use
   - Contact Special Collections

Email: rbml@columbia.edu
```

---

##### E. Internet Archive (Archive.org)
**URL:** [https://archive.org](https://archive.org)

**What They Have:**
- ~500+ Ambedkar-related items (books, speeches, documents)
- Some digitized manuscripts
- Audio/video recordings

**How to Access:**
```
BULK DOWNLOAD:

1. Search:
   site:archive.org Ambedkar

2. Advanced Search Filters:
   - Creator: Ambedkar
   - Language: English/Hindi/Marathi
   - Format: PDF, Text, Audio

3. Bulk Download via API:
   - Python: internetarchive library
   - Check each item's license before use
   - Most materials are public domain
```

---

##### F. Google Books / Internet Archive Scholar
**URL:** [https://scholar.google.com](https://scholar.google.com)

**What They Have:**
- Scholarly articles about Ambedkar
- Books (some full-text available)
- Research papers

**How to Access:**
```
ACADEMIC SEARCH:

1. Search queries:
   - "Dr. Ambedkar" + Constitution
   - "Ambedkar" + Social Justice
   - "Ambedkar" + Annihilation of Caste

2. Filter:
   - Free full-text articles
   - Recent research
   - Sort by relevance

3. Extract:
   - Citations and metadata
   - Download PDFs (where available)
   - Build bibliography for context
```

---

#### **TIER 2: SUPPORTING DATA SOURCES**

##### University Libraries in India
```
IIT Bombay Library: Ambedkar Center materials
Delhi University Library: Constitutional studies
Jawaharlal Nehru University: Social justice research
TISS Mumbai: Social work perspective
```

##### Government Data Sources
```
Ministry of Social Justice publications
Planning Commission documents
Census of India (for demographic context)
```

---

### 1.2 Practical Data Collection Steps

#### **WEEK 1: Rapid Data Acquisition**

```markdown
MONDAY-TUESDAY:
□ Email Dr. Ambedkar Foundation requesting data
□ Scan Lok Sabha CAD website for available downloads
□ Register with NDL (if needed)
□ Document all contact information

WEDNESDAY-THURSDAY:
□ Run NDL API queries (see code below)
□ Download CAD PDFs from Lok Sabha site
□ Search Internet Archive programmatically
□ Compile all metadata into spreadsheet

FRIDAY:
□ Organize collected data by format
□ Create data inventory spreadsheet
□ Identify gaps
□ Plan Week 2 acquisition
```

---

## PART 2: SAMPLE CODE FOR DATA ACQUISITION

### 2.1 NDL (National Digital Library) Data Extraction

#### Python Script - NDL API Access

```python
import requests
import json
import pandas as pd
from datetime import datetime

class NDLDataCollector:
    """Fetch Ambedkar-related materials from NDL"""
    
    def __init__(self):
        self.base_url = "https://www.ndl.iitkgp.ac.in/api/search"
        self.all_data = []
    
    def search_ndl(self, query, pages=5):
        """
        Search NDL for Ambedkar materials
        
        Args:
            query (str): Search term (e.g., "Ambedkar")
            pages (int): Number of pages to fetch (default 5)
        """
        print(f"Searching NDL for: {query}")
        
        for page in range(1, pages + 1):
            params = {
                "q": query,
                "rpp": 100,  # Results per page (max 100)
                "page": page
            }
            
            try:
                response = requests.get(self.base_url, params=params, timeout=10)
                data = response.json()
                
                if "response" in data and "docs" in data["response"]:
                    docs = data["response"]["docs"]
                    print(f"Page {page}: Found {len(docs)} documents")
                    
                    for doc in docs:
                        self.all_data.append({
                            "title": doc.get("title", "N/A"),
                            "author": doc.get("author", "N/A"),
                            "publisher": doc.get("publisher", "N/A"),
                            "year": doc.get("year", "N/A"),
                            "language": doc.get("language", "N/A"),
                            "url": doc.get("url", "N/A"),
                            "resource_type": doc.get("resourceType", "N/A"),
                            "source": "NDL"
                        })
                
                if len(docs) < 100:  # Last page
                    break
                    
            except Exception as e:
                print(f"Error on page {page}: {e}")
                continue
        
        return self.all_data
    
    def search_multiple_queries(self, queries):
        """Search multiple related terms"""
        for query in queries:
            self.search_ndl(query, pages=3)
        
        return self.all_data
    
    def save_to_csv(self, filename="ndl_ambedkar_data.csv"):
        """Save collected data to CSV"""
        df = pd.DataFrame(self.all_data)
        df.to_csv(filename, index=False)
        print(f"Saved {len(df)} records to {filename}")
        return df
    
    def save_to_json(self, filename="ndl_ambedkar_data.json"):
        """Save collected data to JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.all_data, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(self.all_data)} records to {filename}")

# Usage
if __name__ == "__main__":
    collector = NDLDataCollector()
    
    # Search for Ambedkar-related materials
    queries = [
        "Dr. Ambedkar",
        "B.R. Ambedkar",
        "Ambedkar Constitution",
        "Annihilation of Caste",
        "Buddha and His Dhamma"
    ]
    
    collector.search_multiple_queries(queries)
    df = collector.save_to_csv()
    collector.save_to_json()
    
    print(f"\nTotal records collected: {len(collector.all_data)}")
    print(f"Languages found: {df['language'].unique()}")
    print(f"Resource types: {df['resource_type'].unique()}")
```

---

### 2.2 Lok Sabha CAD (Constituent Assembly Debates) Extraction

```python
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

class CADExtractor:
    """Extract and structure Constituent Assembly Debates"""
    
    def __init__(self):
        self.base_url = "https://www.loksabha.gov.in/DisplayCAD"
        self.debates = []
    
    def get_cad_volumes(self):
        """Fetch list of all CAD volumes"""
        try:
            response = requests.get(self.base_url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Parse available volumes
            volumes = []
            # Note: Exact HTML structure may vary - inspect website first
            volume_links = soup.find_all('a', href=re.compile(r'CAD.*\.pdf'))
            
            for link in volume_links:
                volumes.append({
                    'name': link.text,
                    'url': link.get('href')
                })
            
            return volumes
        
        except Exception as e:
            print(f"Error fetching volumes: {e}")
            return []
    
    def extract_ambedkar_speeches(self, volume_url):
        """
        Extract Ambedkar's speeches from a CAD volume PDF
        (Using PDF processing)
        """
        try:
            import PyPDF2
            
            response = requests.get(volume_url)
            pdf_reader = PyPDF2.PdfReader(response.content)
            
            ambedkar_content = []
            
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                
                # Search for Ambedkar's name and following content
                if "AMBEDKAR" in text.upper() or "DR. B.R." in text:
                    ambedkar_content.append({
                        'volume': volume_url.split('/')[-1],
                        'page': page_num + 1,
                        'content': text,
                        'source': 'CAD'
                    })
            
            return ambedkar_content
        
        except Exception as e:
            print(f"Error extracting from PDF: {e}")
            return []
    
    def structure_debate_entry(self, raw_entry):
        """Structure raw debate entry into organized format"""
        return {
            'date': extract_date(raw_entry['content']),
            'speaker': 'Dr. B.R. Ambedkar',
            'topic': extract_topic(raw_entry['content']),
            'content': raw_entry['content'],
            'volume': raw_entry['volume'],
            'page': raw_entry['page'],
            'language': 'English',
            'document_type': 'Constitutional Debate',
            'metadata': {
                'source': 'Lok Sabha CAD',
                'collection': 'Constituent Assembly Records',
                'accessibility': 'public_domain'
            }
        }

def extract_date(text):
    """Extract date from debate text"""
    import re
    dates = re.findall(r'\d{1,2}(?:st|nd|rd|th)?\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}', text)
    return dates[0] if dates else "Unknown"

def extract_topic(text):
    """Extract debate topic"""
    lines = text.split('\n')
    for line in lines[:5]:
        if len(line) > 20 and len(line) < 100:
            return line.strip()
    return "Ambedkar Speech"

# Usage
if __name__ == "__main__":
    extractor = CADExtractor()
    volumes = extractor.get_cad_volumes()
    print(f"Found {len(volumes)} CAD volumes")
```

---

### 2.3 Internet Archive Bulk Download

```python
import internetarchive as ia
import json
import os

class InternetArchiveCollector:
    """Download Ambedkar materials from Internet Archive"""
    
    def __init__(self):
        self.items = []
    
    def search_internet_archive(self, query, limit=100):
        """Search Internet Archive"""
        try:
            search_results = ia.search_items(query)
            
            for item in search_results[:limit]:
                item_data = {
                    'identifier': item.identifier,
                    'title': item.get('title', 'N/A'),
                    'creator': item.get('creator', 'N/A'),
                    'date': item.get('date', 'N/A'),
                    'description': item.get('description', 'N/A'),
                    'language': item.get('language', 'en'),
                    'url': f"https://archive.org/details/{item.identifier}",
                    'mediatype': item.get('mediatype', 'N/A')
                }
                self.items.append(item_data)
                print(f"Found: {item_data['title']}")
            
            return self.items
        
        except Exception as e:
            print(f"Error searching Internet Archive: {e}")
            return []
    
    def download_item(self, identifier, output_dir="downloads/"):
        """Download an item from Internet Archive"""
        try:
            item = ia.get_item(identifier)
            
            # Create output directory
            os.makedirs(output_dir, exist_ok=True)
            
            # Download all files
            for file in item.get_files():
                if file.format in ['PDF', 'Text PDF', 'EPUB']:
                    file_path = os.path.join(output_dir, file.name)
                    print(f"Downloading: {file.name}")
                    item.download(file_basename=file.name, destdir=output_dir)
            
            return True
        
        except Exception as e:
            print(f"Error downloading {identifier}: {e}")
            return False
    
    def bulk_download(self, identifiers, output_dir="downloads/"):
        """Download multiple items"""
        for identifier in identifiers:
            self.download_item(identifier, output_dir)
    
    def save_metadata(self, filename="ia_metadata.json"):
        """Save all metadata"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.items, f, indent=2, ensure_ascii=False)
        print(f"Metadata saved to {filename}")

# Usage
if __name__ == "__main__":
    ia.configure(None, None)  # No auth needed for public items
    
    collector = InternetArchiveCollector()
    
    # Search for Ambedkar materials
    collector.search_internet_archive('Ambedkar', limit=50)
    
    # Save metadata
    collector.save_metadata()
    
    # Download a few items
    # collector.bulk_download(['item_id_1', 'item_id_2'])
```

---

### 2.4 Data Organization Script

```python
import os
import json
import pandas as pd
from datetime import datetime

class DataOrganizer:
    """Organize collected data into structured format"""
    
    def __init__(self, base_dir="ambedkar_archive_data"):
        self.base_dir = base_dir
        self.metadata = []
        self.create_directory_structure()
    
    def create_directory_structure(self):
        """Create organized directory structure"""
        directories = [
            f"{self.base_dir}/raw_documents",
            f"{self.base_dir}/processed_data",
            f"{self.base_dir}/metadata",
            f"{self.base_dir}/images",
            f"{self.base_dir}/audio_video",
            f"{self.base_dir}/texts",
            f"{self.base_dir}/scripts"
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            print(f"Created: {directory}")
    
    def organize_by_source(self, source_data):
        """Organize data by source"""
        organized = {
            'ndl': [],
            'cad': [],
            'internet_archive': [],
            'foundation': [],
            'columbia': []
        }
        
        for item in source_data:
            source = item.get('source', 'unknown').lower()
            if source in organized:
                organized[source].append(item)
        
        return organized
    
    def organize_by_type(self, data):
        """Organize by document type"""
        organized = {
            'manuscripts': [],
            'speeches': [],
            'debates': [],
            'letters': [],
            'publications': [],
            'audio': [],
            'video': [],
            'images': []
        }
        
        type_map = {
            'manuscript': 'manuscripts',
            'speech': 'speeches',
            'debate': 'debates',
            'letter': 'letters',
            'book': 'publications',
            'article': 'publications'
        }
        
        for item in data:
            doc_type = item.get('type', 'unknown').lower()
            category = type_map.get(doc_type, 'publications')
            organized[category].append(item)
        
        return organized
    
    def create_metadata_registry(self, all_data):
        """Create master metadata registry"""
        registry = {
            'created': datetime.now().isoformat(),
            'total_items': len(all_data),
            'sources': {},
            'types': {},
            'languages': {},
            'data': all_data
        }
        
        # Count by source
        for item in all_data:
            source = item.get('source', 'unknown')
            registry['sources'][source] = registry['sources'].get(source, 0) + 1
        
        # Count by type
        for item in all_data:
            doc_type = item.get('type', 'unknown')
            registry['types'][doc_type] = registry['types'].get(doc_type, 0) + 1
        
        # Count by language
        for item in all_data:
            lang = item.get('language', 'unknown')
            registry['languages'][lang] = registry['languages'].get(lang, 0) + 1
        
        # Save registry
        with open(f"{self.base_dir}/metadata/registry.json", 'w', encoding='utf-8') as f:
            json.dump(registry, f, indent=2, ensure_ascii=False)
        
        print(f"Created metadata registry with {len(all_data)} items")
        return registry
    
    def generate_data_inventory(self):
        """Generate inventory report"""
        report = {
            'collection_date': datetime.now().isoformat(),
            'total_documents': 0,
            'by_source': {},
            'by_type': {},
            'by_language': {},
            'storage_location': self.base_dir,
            'next_steps': [
                'Digitize physical documents',
                'Apply OCR to images',
                'Extract metadata',
                'Create indices',
                'Build search functionality'
            ]
        }
        
        print("\n" + "="*50)
        print("DATA INVENTORY REPORT")
        print("="*50)
        print(json.dumps(report, indent=2))
        
        return report

# Usage
if __name__ == "__main__":
    organizer = DataOrganizer()
    
    # Load all collected data (from previous scripts)
    all_data = []  # Combine NDL, CAD, IA data here
    
    # Create registry
    organizer.create_metadata_registry(all_data)
    
    # Generate report
    organizer.generate_data_inventory()
```

---

## PART 3: IMPLEMENTATION ACROSS PLATFORMS

### 3.1 CLAUDE CODE Implementation

#### Setup & Installation

```bash
# Install Claude Code (if not already installed)
npm install -g @anthropic-ai/claude-code

# OR using pip
pip install anthropic-claude-code

# Verify installation
claude-code --version
```

#### Project Structure for Claude Code

```
ambedkar-archive-claude/
├── src/
│   ├── data_collection/
│   │   ├── ndl_collector.py
│   │   ├── cad_extractor.py
│   │   └── ia_downloader.py
│   ├── backend/
│   │   ├── app.py (FastAPI)
│   │   ├── models.py
│   │   ├── routes.py
│   │   └── database.py
│   ├── frontend/
│   │   ├── index.html
│   │   ├── styles.css
│   │   └── app.js
│   └── ml/
│       ├── ocr_processor.py
│       ├── semantic_search.py
│       └── translation_service.py
├── requirements.txt
├── claude-code.yaml
└── README.md
```

#### Claude Code Workflow

```yaml
# claude-code.yaml
project:
  name: "Ambedkar Digital Archive"
  description: "AI-powered heritage archive system"
  version: "0.1.0"

commands:
  setup:
    description: "Install dependencies"
    commands:
      - "pip install -r requirements.txt"
  
  data_collect:
    description: "Collect data from sources"
    commands:
      - "python src/data_collection/ndl_collector.py"
      - "python src/data_collection/cad_extractor.py"
  
  server:
    description: "Start backend server"
    command: "python src/backend/app.py"
  
  test:
    description: "Run tests"
    command: "pytest tests/"

files_to_create:
  - path: "src/backend/app.py"
    template: "fastapi_app"
  - path: "src/frontend/index.html"
    template: "html_page"
  - path: "requirements.txt"
    content: |
      fastapi==0.104.0
      uvicorn==0.24.0
      requests==2.31.0
      pandas==2.1.0
      beautifulsoup4==4.12.0
      PyPDF2==4.0.1
      elasticsearch==8.11.0
      google-cloud-translate==3.14.0
      pytesseract==0.3.10
```

#### Claude Code: FastAPI Backend Example

```python
# src/backend/app.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import json
import os

app = FastAPI(title="Ambedkar Digital Archive API")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============ DATA MODELS ============

class Document(BaseModel):
    id: str
    title: str
    author: str
    content: str
    language: str
    document_type: str
    date: Optional[str] = None
    tags: List[str] = []

class SearchQuery(BaseModel):
    q: str
    language: Optional[str] = None
    document_type: Optional[str] = None
    limit: int = 20

class SearchResult(BaseModel):
    total: int
    results: List[Document]
    query: str

# ============ DATA STORAGE (In-memory for MVP) ============

# In production, use PostgreSQL or MongoDB
documents_store = []

# Load metadata from collected data
def load_documents():
    """Load documents from local metadata files"""
    try:
        if os.path.exists('ambedkar_archive_data/metadata/registry.json'):
            with open('ambedkar_archive_data/metadata/registry.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('data', [])
    except Exception as e:
        print(f"Error loading documents: {e}")
    return []

# ============ ROUTES ============

@app.on_event("startup")
async def startup_event():
    """Load documents on startup"""
    global documents_store
    documents_store = load_documents()
    print(f"Loaded {len(documents_store)} documents")

@app.get("/")
async def root():
    """API health check"""
    return {
        "status": "running",
        "version": "0.1.0",
        "name": "Ambedkar Digital Archive API"
    }

@app.get("/api/stats")
async def get_stats():
    """Get archive statistics"""
    stats = {
        "total_documents": len(documents_store),
        "languages": {},
        "types": {},
        "sources": {}
    }
    
    for doc in documents_store:
        # Count by language
        lang = doc.get('language', 'unknown')
        stats['languages'][lang] = stats['languages'].get(lang, 0) + 1
        
        # Count by type
        doc_type = doc.get('type', 'unknown')
        stats['types'][doc_type] = stats['types'].get(doc_type, 0) + 1
        
        # Count by source
        source = doc.get('source', 'unknown')
        stats['sources'][source] = stats['sources'].get(source, 0) + 1
    
    return stats

@app.post("/api/search")
async def search_documents(query: SearchQuery) -> SearchResult:
    """
    Search documents with semantic understanding
    
    Parameters:
    - q: Search query
    - language: Filter by language
    - document_type: Filter by type
    - limit: Max results to return
    """
    
    search_term = query.q.lower()
    results = []
    
    for doc in documents_store:
        # Apply filters
        if query.language and doc.get('language') != query.language:
            continue
        
        if query.document_type and doc.get('type') != query.document_type:
            continue
        
        # Simple keyword matching (Replace with semantic search)
        if (search_term in doc.get('title', '').lower() or
            search_term in doc.get('content', '').lower() or
            search_term in ' '.join(doc.get('tags', [])).lower()):
            results.append(doc)
    
    # Sort by relevance (TODO: implement proper relevance ranking)
    results = results[:query.limit]
    
    return SearchResult(
        total=len(results),
        results=results,
        query=query.q
    )

@app.get("/api/documents/{doc_id}")
async def get_document(doc_id: str):
    """Get a specific document"""
    for doc in documents_store:
        if doc.get('id') == doc_id:
            return doc
    raise HTTPException(status_code=404, detail="Document not found")

@app.get("/api/documents")
async def list_documents(skip: int = 0, limit: int = 50, language: Optional[str] = None):
    """List all documents with pagination"""
    filtered = documents_store
    
    if language:
        filtered = [d for d in filtered if d.get('language') == language]
    
    return {
        "total": len(filtered),
        "items": filtered[skip:skip + limit],
        "skip": skip,
        "limit": limit
    }

@app.get("/api/languages")
async def get_languages():
    """Get available languages"""
    languages = set()
    for doc in documents_store:
        languages.add(doc.get('language', 'unknown'))
    return {"languages": sorted(list(languages))}

@app.get("/api/document-types")
async def get_document_types():
    """Get available document types"""
    types = set()
    for doc in documents_store:
        types.add(doc.get('type', 'unknown'))
    return {"types": sorted(list(types))}

# ============ RUN SERVER ============

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

#### Claude Code: Frontend Example

```html
<!-- src/frontend/index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ambedkar Digital Archive</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div id="app">
        <header class="header">
            <h1>Dr. B.R. Ambedkar Digital Archive</h1>
            <p>Preserving Constitutional Thought. Democratizing Access.</p>
        </header>

        <nav class="navbar">
            <button onclick="showSection('search')">Search</button>
            <button onclick="showSection('browse')">Browse</button>
            <button onclick="showSection('about')">About</button>
            <button onclick="showSection('stats')">Statistics</button>
        </nav>

        <!-- Search Section -->
        <section id="search" class="section active">
            <h2>Search Archives</h2>
            <div class="search-container">
                <input type="text" id="searchInput" placeholder="Search for documents...">
                <select id="languageFilter">
                    <option value="">All Languages</option>
                    <option value="en">English</option>
                    <option value="hi">Hindi</option>
                    <option value="mr">Marathi</option>
                </select>
                <select id="typeFilter">
                    <option value="">All Types</option>
                    <option value="speech">Speeches</option>
                    <option value="manuscript">Manuscripts</option>
                    <option value="debate">Debates</option>
                </select>
                <button onclick="performSearch()">Search</button>
            </div>
            <div id="searchResults" class="results-container"></div>
        </section>

        <!-- Browse Section -->
        <section id="browse" class="section">
            <h2>Browse Documents</h2>
            <div id="documentList" class="document-list"></div>
        </section>

        <!-- Statistics Section -->
        <section id="stats" class="section">
            <h2>Archive Statistics</h2>
            <div id="statsContainer" class="stats-container"></div>
        </section>

        <!-- About Section -->
        <section id="about" class="section">
            <h2>About This Archive</h2>
            <p>This digital archive preserves and makes accessible the works of Dr. B.R. Ambedkar...</p>
        </section>
    </div>

    <script src="app.js"></script>
</body>
</html>
```

---

### 3.2 GOOGLE COLAB Implementation

#### Setup Notebook

```python
# Cell 1: Install Dependencies
!pip install requests pandas beautifulsoup4 PyPDF2
!pip install elasticsearch google-cloud-translate
!pip install pytesseract pillow
!pip install fastapi uvicorn
!pip install internetarchive

# Also install OCR
!apt-get install -y tesseract-ocr
```

#### Data Collection in Colab

```python
# Cell 2: Mount Google Drive
from google.colab import drive
drive.mount('/content/drive')

# Create working directory
import os
os.makedirs('/content/ambedkar_archive', exist_ok=True)

# Cell 3: NDL Data Collection
import requests
import pandas as pd
import json

def collect_ndl_data():
    """Collect data from National Digital Library"""
    base_url = "https://www.ndl.iitkgp.ac.in/api/search"
    
    queries = [
        "Dr. Ambedkar",
        "B.R. Ambedkar",
        "Constitutional Assembly Debates"
    ]
    
    all_data = []
    
    for query in queries:
        params = {
            "q": query,
            "rpp": 50,
            "page": 1
        }
        
        try:
            response = requests.get(base_url, params=params, timeout=10)
            data = response.json()
            
            if "response" in data:
                for doc in data["response"].get("docs", []):
                    all_data.append({
                        'title': doc.get('title', 'N/A'),
                        'author': doc.get('author', 'N/A'),
                        'year': doc.get('year', 'N/A'),
                        'language': doc.get('language', 'en'),
                        'url': doc.get('url', 'N/A'),
                        'source': 'NDL'
                    })
        except Exception as e:
            print(f"Error fetching {query}: {e}")
    
    df = pd.DataFrame(all_data)
    df.to_csv('/content/ambedkar_archive/ndl_data.csv', index=False)
    print(f"Collected {len(df)} documents from NDL")
    return df

# Run collection
ndl_df = collect_ndl_data()
ndl_df.head()

# Cell 4: Internet Archive Collection
import internetarchive as ia

def collect_ia_data():
    """Collect from Internet Archive"""
    ia.configure(None, None)
    
    search_results = ia.search_items('Ambedkar')
    
    ia_data = []
    for item in search_results:
        ia_data.append({
            'identifier': item.identifier,
            'title': item.get('title', 'N/A'),
            'creator': item.get('creator', 'N/A'),
            'date': item.get('date', 'N/A'),
            'mediatype': item.get('mediatype', 'N/A'),
            'url': f"https://archive.org/details/{item.identifier}",
            'source': 'Internet Archive'
        })
    
    df = pd.DataFrame(ia_data)
    df.to_csv('/content/ambedkar_archive/ia_data.csv', index=False)
    print(f"Collected {len(df)} items from Internet Archive")
    return df

ia_df = collect_ia_data()
ia_df.head()

# Cell 5: Combine All Data
combined_df = pd.concat([ndl_df, ia_df], ignore_index=True)
combined_df.to_csv('/content/ambedkar_archive/combined_metadata.csv', index=False)

print(f"\nTotal documents collected: {len(combined_df)}")
print(f"\nLanguages: {combined_df['language'].unique()}")
print(f"\nSources: {combined_df['source'].value_counts()}")
```

#### OCR and Text Processing in Colab

```python
# Cell 6: OCR Processing
from PIL import Image
import pytesseract
import cv2
import numpy as np

def process_image_ocr(image_path):
    """Extract text from image using Tesseract"""
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img, lang='eng+hin')
        return text
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return ""

def preprocess_image(image_path):
    """Preprocess image for better OCR"""
    img = cv2.imread(image_path, 0)
    # Apply thresholding
    _, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    return img

# Cell 7: Multilingual Translation
from google.cloud import translate_v2
import os

# Note: Requires Google Cloud credentials
# For Colab, use free API or local alternatives

def translate_text(text, target_language='hi'):
    """Translate text to target language"""
    # Using free Google Translate API (via requests)
    try:
        from google.colab import auth
        auth.authenticate_user()
        
        translate_client = translate_v2.Client()
        result = translate_client.translate_text(
            text,
            target_language=target_language
        )
        return result['translatedText']
    except:
        print("Translation requires credentials. Use alternative API.")
        return text

# Alternative: Use free translation API
def translate_free(text, target_lang='hi'):
    """Free translation using LibreTranslate or Google API"""
    # Using Google Translate API (limited free tier)
    try:
        from google.colab import auth
        from google.cloud import translate
        
        client = translate.TranslationServiceClient()
        
        project_id = "your-project-id"  # Set your project
        
        response = client.translate_text(
            request={
                "parent": f"projects/{project_id}",
                "contents": [text],
                "mime_type": "text/plain",
                "source_language_code": "en",
                "target_language_code": target_lang,
            }
        )
        
        return response.translations[0].translated_text
    except:
        print("Translation API not configured")
        return text
```

#### Colab: Deploy to Cloud

```python
# Cell 8: Create and Deploy Simple API
!pip install flask flask-cors

# Create Flask app
app_code = '''
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import json

app = Flask(__name__)
CORS(app)

# Load data
df = pd.read_csv('/content/ambedkar_archive/combined_metadata.csv')

@app.route('/')
def home():
    return {'status': 'Ambedkar Archive API Running'}

@app.route('/api/search', methods=['POST'])
def search():
    data = request.json
    query = data.get('q', '').lower()
    
    results = df[
        (df['title'].str.lower().str.contains(query, na=False)) |
        (df['author'].str.lower().str.contains(query, na=False))
    ]
    
    return {
        'total': len(results),
        'results': results.head(20).to_dict('records')
    }

@app.route('/api/stats', methods=['GET'])
def stats():
    return {
        'total_documents': len(df),
        'languages': df['language'].value_counts().to_dict(),
        'sources': df['source'].value_counts().to_dict()
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
'''

with open('/content/app.py', 'w') as f:
    f.write(app_code)

# Run with ngrok for public URL
!pip install pyngrok

from pyngrok import ngrok
ngrok.set_auth_token('YOUR_NGROK_TOKEN')  # Get from https://ngrok.com

public_url = ngrok.connect(5000)
print(f"Public URL: {public_url}")

# Cell 9: Run Flask Server
import subprocess
import time

# Start Flask in background
process = subprocess.Popen(['python', '/content/app.py'], 
                          stdout=subprocess.PIPE, 
                          stderr=subprocess.PIPE)

time.sleep(3)  # Wait for server to start

# Test the API
import requests
response = requests.get('http://localhost:5000')
print("Server Status:", response.json())
```

---

### 3.3 ANTHROPIC TOOLS & APIs

#### Using Claude API for Content Processing

```python
import anthropic
import json

client = anthropic.Anthropic(api_key="your-api-key")

def analyze_ambedkar_document(document_text, language='en'):
    """
    Use Claude to analyze and summarize Ambedkar documents
    """
    
    prompt = f"""
    Analyze this document from Dr. B.R. Ambedkar:
    
    DOCUMENT:
    {document_text}
    
    Please provide:
    1. Main themes and concepts
    2. Key arguments
    3. Historical context
    4. Relevance to constitutional law
    5. Summary (2-3 sentences)
    6. Suggested tags/categories
    
    Respond in JSON format.
    """
    
    message = client.messages.create(
        model="claude-opus-4-6",  # Or latest model
        max_tokens=2000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    response_text = message.content[0].text
    
    # Parse JSON from response
    try:
        # Extract JSON from response
        import re
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            analysis = json.loads(json_match.group())
            return analysis
    except:
        return {"raw_analysis": response_text}

def generate_timeline(documents):
    """Generate chronological timeline from documents"""
    
    doc_list = "\n".join([f"- {d.get('title')}: {d.get('date', 'Unknown date')}" 
                          for d in documents])
    
    prompt = f"""
    Create a chronological timeline from these Dr. Ambedkar works:
    
    {doc_list}
    
    Format as JSON with:
    - year
    - event
    - significance
    - related_works (list)
    """
    
    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1500,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return message.content[0].text

def create_research_guide(topic):
    """Generate interactive research guide using Claude"""
    
    prompt = f"""
    Create an interactive research guide for: {topic}
    
    Based on Dr. B.R. Ambedkar's work, provide:
    1. Overview
    2. Key primary sources
    3. Important concepts
    4. Discussion questions
    5. Further reading suggestions
    
    Format as structured JSON for an educational interface.
    """
    
    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=2500,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return message.content[0].text
```

---

## PART 4: IMMEDIATE NEXT STEPS (WEEK 1-2)

### Week 1: Data Foundation

```
MONDAY:
□ Send formal data requests to Dr. Ambedkar Foundation
□ Register with NDL and Internet Archive accounts
□ Create Google Colab notebook
□ Set up GitHub repository

TUESDAY-WEDNESDAY:
□ Run NDL API collection script
□ Download CAD PDFs from Lok Sabha
□ Scrape Internet Archive for Ambedkar materials
□ Begin organizing data into directory structure

THURSDAY-FRIDAY:
□ Create metadata registry (CSV/JSON)
□ Organize documents by type, language, source
□ Generate data inventory report
□ Document data acquisition process
```

### Week 2: MVP Development

```
MONDAY-TUESDAY:
□ Set up Flask/FastAPI backend
□ Create basic search API
□ Build simple HTML frontend
□ Implement keyword search

WEDNESDAY-THURSDAY:
□ Add multilingual support (language filters)
□ Integrate OCR for sample documents
□ Create document detail page
□ Add statistics dashboard

FRIDAY:
□ Deploy to Colab or Claude Code
□ Test end-to-end workflow
□ Prepare demo for judges
□ Document technical approach
```

---

## PART 5: TOOL COMPARISON & RECOMMENDATIONS

### Claude Code vs. Google Colab vs. Local Development

| Aspect | Claude Code | Google Colab | Local/Anthripic |
|--------|-----------|--------------|----------|
| **Setup Time** | Fastest | Very Fast | Moderate |
| **Data Storage** | Cloud | Drive Integration | Local/Custom |
| **GPU/Computing** | Good | Excellent | Depends |
| **Real-time Debugging** | Excellent | Good | Excellent |
| **AI Integration** | Native Claude API | Limited | Full API Access |
| **Deployment** | Easy | Built-in | More Work |
| **Best For** | MVP + Full App | Data Analysis | Production |
| **Cost** | API pricing | Free | API pricing |

### Recommendation for This Project

🟢 **Start with Google Colab** (Week 1-2)
- Fast data collection and processing
- Easy to share and collaborate
- Can deploy to Ngrok quickly

🟢 **Move to Claude Code** (Week 2-3)
- Build full-stack application
- Leverage Claude API for content analysis
- Create production-ready code

🟢 **Use Anthropic API** (Week 3+)
- Fine-tune document analysis
- Create AI-powered research assistant
- Integrate with backend

---

## PART 6: FREE/OPEN DATA SOURCES (Complete List)

```
1. National Digital Library (NDL)
   - API: https://www.ndl.iitkgp.ac.in/api/docs
   - Free, public domain materials
   
2. Internet Archive
   - Bulk download API
   - Hundreds of public domain books
   
3. Lok Sabha CAD Website
   - Complete constitutional debates (public)
   - Free PDFs available
   
4. Google Books (partial)
   - Some Ambedkar books with preview
   - Free content download available
   
5. Project Gutenberg
   - Some public domain texts
   - Ambedkar-related materials
   
6. Open Library (openlibrary.org)
   - APIs for book metadata
   - Some full texts available
   
7. Wikipedia Commons
   - Ambedkar images and documents
   - All free to use with attribution
```

---

## PART 7: SAMPLE DATA SCHEMA

```json
{
  "document": {
    "id": "UNIQUE_ID",
    "title": "Document Title",
    "author": "Dr. B.R. Ambedkar",
    "date": "1950-01-26",
    "type": "speech|manuscript|debate|publication|letter|other",
    "language": "en|hi|mr|ta|te|ka|bn|gu|pa|ml",
    "content": {
      "full_text": "...",
      "summary": "...",
      "key_quotes": ["...", "..."]
    },
    "metadata": {
      "source": "NDL|CAD|Foundation|IA|Columbia",
      "archive_reference": "...",
      "collection": "...",
      "pages": 15,
      "word_count": 5000,
      "condition": "good|fair|poor",
      "accessibility": "public|restricted"
    },
    "tags": [
      "constitutional",
      "social_justice",
      "equality",
      "rights",
      "dalits",
      "caste"
    ],
    "relations": {
      "references": ["doc_id_1", "doc_id_2"],
      "related_to": ["doc_id_3"],
      "debates": ["debate_id_1"]
    },
    "translations": {
      "hi": {
        "title": "...",
        "summary": "...",
        "text_url": "..."
      }
    },
    "media": {
      "images": ["url1", "url2"],
      "audio": "url_to_audio",
      "video": "url_to_video"
    }
  }
}
```

---

## PART 8: SUCCESS METRICS & CHECKLIST

### Week 1 Completion Checklist
- [ ] 500+ documents collected from NDL
- [ ] CAD PDFs downloaded and organized
- [ ] Internet Archive metadata extracted (100+ items)
- [ ] Metadata registry created (JSON + CSV)
- [ ] Data organized by type, language, source
- [ ] Documentation of data sources
- [ ] GitHub repo with data collection scripts

### Week 2 Completion Checklist
- [ ] FastAPI/Flask backend running
- [ ] Basic keyword search working
- [ ] Frontend UI with search interface
- [ ] Deployed to Colab or Claude Code
- [ ] Statistics dashboard showing data breakdown
- [ ] OCR working on sample documents
- [ ] Multilingual support for 2+ languages

### Week 3+ (Post-Hackathon)
- [ ] Semantic search implementation
- [ ] AI-powered Q&A system
- [ ] Full multilingual support (6-8 languages)
- [ ] Audio/video archival
- [ ] Interactive timeline
- [ ] Production deployment
- [ ] Government integration ready

---

## PART 9: TROUBLESHOOTING & COMMON ISSUES

### Issue: API Rate Limiting
```python
# Solution: Add rate limiting logic
import time

def api_call_with_retry(url, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return response.json()
        except:
            time.sleep(2 ** attempt)  # Exponential backoff
    return None
```

### Issue: Large PDF Processing
```python
# Solution: Process in chunks
def process_large_pdf(pdf_path, chunk_size=10):
    pdf = PyPDF2.PdfReader(pdf_path)
    text_chunks = []
    
    for page_num in range(0, len(pdf.pages), chunk_size):
        chunk_text = ""
        for i in range(page_num, min(page_num + chunk_size, len(pdf.pages))):
            chunk_text += pdf.pages[i].extract_text()
        text_chunks.append(chunk_text)
    
    return text_chunks
```

### Issue: Multilingual Character Encoding
```python
# Solution: Ensure UTF-8 encoding
def save_with_encoding(data, filename, encoding='utf-8'):
    with open(filename, 'w', encoding=encoding) as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
```

---

## FINAL ACTION PLAN

### RIGHT NOW (Today)
1. ✅ Read this guide completely
2. ✅ Choose platform: Google Colab OR Claude Code
3. ✅ Create account (Google/Anthropic)
4. ✅ Set up first notebook/project

### TOMORROW
1. 📧 Email data source requests
2. 🔧 Run NDL collection script
3. 📊 Create data inventory
4. 📝 Document findings

### THIS WEEK
1. 🔍 Collect 500+ documents
2. 🛠️ Build MVP backend
3. 🎨 Create basic frontend
4. 🚀 Deploy to Colab/Claude Code

### NEXT WEEK
1. 🤖 Add AI/ML features
2. 🌍 Implement multilingual support
3. 🎯 Create compelling demo
4. 📊 Prepare presentation

---

**Remember:** You're not just building a technical project. You're democratizing access to foundational constitutional thought. That's meaningful. That's impactful. Go build something great! 🚀
