import React, { useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import {
  Archive, Search, Upload, BookOpen, Database, Languages,
  FolderOpen, X, FileText, Trash2, ExternalLink
} from "lucide-react";
import "./styles.css";

const API = "/api";

function App() {
  const [documents, setDocuments] = useState([]);
  const [stats, setStats] = useState({ documents: 0, languages: 0, collections: 0 });
  const [query, setQuery] = useState("");
  const [collection, setCollection] = useState("");
  const [collections, setCollections] = useState([]);
  const [selected, setSelected] = useState(null);
  const [showUpload, setShowUpload] = useState(false);
  const [loading, setLoading] = useState(false);

  async function load(filters = {}) {
    setLoading(true);
    const params = new URLSearchParams();
    if (filters.q !== undefined) params.set("q", filters.q);
    if (filters.collection !== undefined) params.set("collection", filters.collection);

    const [docs, st, cols] = await Promise.all([
      fetch(`${API}/documents?${params}`).then(r => r.json()),
      fetch(`${API}/stats`).then(r => r.json()),
      fetch(`${API}/collections`).then(r => r.json())
    ]);

    setDocuments(docs);
    setStats(st);
    setCollections(cols);
    setLoading(false);
  }

  useEffect(() => { load(); }, []);

  useEffect(() => {
    const t = setTimeout(() => load({ q: query, collection }), 250);
    return () => clearTimeout(t);
  }, [query, collection]);

  async function deleteDoc(id) {
    if (!confirm("Delete this archive record?")) return;
    await fetch(`${API}/documents/${id}`, { method: "DELETE" });
    setSelected(null);
    load({ q: query, collection });
  }

  return (
    <div className="app">
      <header className="topbar">
        <div className="brand">
          <div className="brandIcon"><Archive size={23}/></div>
          <div>
            <h1>Ambedkar Digital Heritage Archive</h1>
            <span>Digital preservation • discovery • research</span>
          </div>
        </div>
        <button className="uploadBtn" onClick={() => setShowUpload(true)}>
          <Upload size={17}/> Upload Record
        </button>
      </header>

      <main>
        <section className="hero">
          <div>
            <div className="eyebrow">DIGITAL HERITAGE PLATFORM</div>
            <h2>Explore, preserve and discover archival knowledge.</h2>
            <p>
              A starter archive platform for organizing documents, metadata and
              searchable historical material related to Dr. B. R. Ambedkar.
            </p>
          </div>
          <div className="heroMark">BR<br/><span>AMBEDKAR</span></div>
        </section>

        <section className="stats">
          <Stat icon={<FileText/>} value={stats.documents} label="Archive records"/>
          <Stat icon={<Languages/>} value={stats.languages} label="Languages"/>
          <Stat icon={<FolderOpen/>} value={stats.collections} label="Collections"/>
          <Stat icon={<Database/>} value={stats.digitized || 0} label="Digitized items"/>
        </section>

        <section className="searchPanel">
          <div className="searchBox">
            <Search size={20}/>
            <input
              value={query}
              onChange={e => setQuery(e.target.value)}
              placeholder="Search title, author, text, collection or tags..."
            />
            {query && <button className="iconBtn" onClick={() => setQuery("")}><X size={18}/></button>}
          </div>
          <select value={collection} onChange={e => setCollection(e.target.value)}>
            <option value="">All collections</option>
            {collections.map(c => <option key={c} value={c}>{c}</option>)}
          </select>
        </section>

        <div className="sectionTitle">
          <div>
            <h3>Archive Collection</h3>
            <p>{loading ? "Searching..." : `${documents.length} records found`}</p>
          </div>
        </div>

        <section className="grid">
          {documents.map(doc => (
            <article className="card" key={doc.id} onClick={() => setSelected(doc)}>
              <div className="cardTop">
                <span className="type">{doc.type}</span>
                {doc.year && <span>{doc.year}</span>}
              </div>
              <h4>{doc.title}</h4>
              <p className="author">{doc.author}</p>
              <p className="description">{doc.description}</p>
              <div className="tags">
                {(doc.tags || []).slice(0, 4).map(t => <span key={t}>#{t}</span>)}
              </div>
              <div className="cardBottom">
                <span>{doc.collection}</span>
                <BookOpen size={17}/>
              </div>
            </article>
          ))}

          {!loading && documents.length === 0 && (
            <div className="empty">
              <Search size={40}/>
              <h3>No records found</h3>
              <p>Try another search or upload a new archival record.</p>
            </div>
          )}
        </section>
      </main>

      {selected && (
        <Modal onClose={() => setSelected(null)}>
          <div className="modalHeader">
            <div>
              <span className="type">{selected.type}</span>
              <h2>{selected.title}</h2>
              <p>{selected.author} {selected.year ? `• ${selected.year}` : ""}</p>
            </div>
            <button className="iconBtn" onClick={() => setSelected(null)}><X/></button>
          </div>
          <div className="metadata">
            <Info label="Collection" value={selected.collection}/>
            <Info label="Language" value={selected.language}/>
            <Info label="Source" value={selected.source}/>
          </div>
          <p className="modalDescription">{selected.description}</p>
          <div className="fullText">
            <h3>Indexed text</h3>
            <p>{selected.text || "No OCR/text content has been added yet."}</p>
          </div>
          {selected.filename && (
            <a className="fileLink" href={`/uploads/${selected.filename}`} target="_blank">
              <ExternalLink size={16}/> Open uploaded file
            </a>
          )}
          <button className="deleteBtn" onClick={() => deleteDoc(selected.id)}>
            <Trash2 size={16}/> Delete record
          </button>
        </Modal>
      )}

      {showUpload && (
        <UploadModal
          onClose={() => setShowUpload(false)}
          onUploaded={() => {
            setShowUpload(false);
            load({ q: query, collection });
          }}
        />
      )}
    </div>
  );
}

function Stat({ icon, value, label }) {
  return <div className="stat"><div className="statIcon">{icon}</div><div><strong>{value}</strong><span>{label}</span></div></div>;
}

function Info({ label, value }) {
  return <div><span>{label}</span><strong>{value || "—"}</strong></div>;
}

function Modal({ children, onClose }) {
  return <div className="overlay" onMouseDown={e => e.target === e.currentTarget && onClose()}>
    <div className="modal">{children}</div>
  </div>;
}

function UploadModal({ onClose, onUploaded }) {
  const [form, setForm] = useState({
    title: "", author: "B. R. Ambedkar", year: "", language: "English",
    collection: "Books & Speeches", type: "Document", description: "",
    tags: "", text: "", source: ""
  });
  const [file, setFile] = useState(null);
  const [saving, setSaving] = useState(false);

  const set = (key, value) => setForm(f => ({ ...f, [key]: value }));

  async function submit(e) {
    e.preventDefault();
    if (!form.title) return alert("Title is required.");
    setSaving(true);
    const data = new FormData();
    Object.entries(form).forEach(([k, v]) => data.append(k, v));
    if (file) data.append("file", file);

    const res = await fetch(`${API}/documents`, { method: "POST", body: data });
    const result = await res.json();
    setSaving(false);

    if (!res.ok) return alert(result.error || "Upload failed.");
    onUploaded();
  }

  return (
    <Modal onClose={onClose}>
      <div className="modalHeader">
        <div><span className="type">ARCHIVE INGESTION</span><h2>Add archival record</h2></div>
        <button className="iconBtn" onClick={onClose}><X/></button>
      </div>
      <form className="form" onSubmit={submit}>
        <label>Title *<input value={form.title} onChange={e => set("title", e.target.value)} /></label>
        <div className="two">
          <label>Author<input value={form.author} onChange={e => set("author", e.target.value)} /></label>
          <label>Year<input type="number" value={form.year} onChange={e => set("year", e.target.value)} /></label>
        </div>
        <div className="two">
          <label>Language<select value={form.language} onChange={e => set("language", e.target.value)}>
            <option>English</option><option>Hindi</option><option>Gujarati</option><option>Marathi</option>
          </select></label>
          <label>Type<select value={form.type} onChange={e => set("type", e.target.value)}>
            <option>Document</option><option>Book</option><option>Speech</option><option>Debate</option><option>Photo</option>
          </select></label>
        </div>
        <label>Collection<input value={form.collection} onChange={e => set("collection", e.target.value)} /></label>
        <label>Tags <small>comma separated</small><input value={form.tags} onChange={e => set("tags", e.target.value)} placeholder="constitution, social reform" /></label>
        <label>Description<textarea rows="2" value={form.description} onChange={e => set("description", e.target.value)} /></label>
        <label>Searchable / OCR text<textarea rows="5" value={form.text} onChange={e => set("text", e.target.value)} placeholder="Paste extracted text here for the MVP..." /></label>
        <label>Source<input value={form.source} onChange={e => set("source", e.target.value)} placeholder="Archive/source name" /></label>
        <label className="fileDrop">Upload file (PDF/JPG/PNG/TXT, max 25 MB)
          <input type="file" accept=".pdf,.jpg,.jpeg,.png,.txt" onChange={e => setFile(e.target.files?.[0] || null)} />
          {file && <span>{file.name}</span>}
        </label>
        <button className="submitBtn" disabled={saving}>{saving ? "Saving..." : "Add to Archive"}</button>
      </form>
    </Modal>
  );
}

createRoot(document.getElementById("root")).render(<App />);