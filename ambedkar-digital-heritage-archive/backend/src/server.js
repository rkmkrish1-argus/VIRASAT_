import express from "express";
import cors from "cors";
import multer from "multer";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import crypto from "crypto";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, "..");
const UPLOADS = path.join(ROOT, "uploads");
const DATA_DIR = path.join(ROOT, "data");
const DATA_FILE = path.join(DATA_DIR, "documents.json");

fs.mkdirSync(UPLOADS, { recursive: true });
fs.mkdirSync(DATA_DIR, { recursive: true });

if (!fs.existsSync(DATA_FILE)) fs.writeFileSync(DATA_FILE, "[]");

const app = express();
app.use(cors());
app.use(express.json());
app.use("/uploads", express.static(UPLOADS));

const storage = multer.diskStorage({
  destination: (_, __, cb) => cb(null, UPLOADS),
  filename: (_, file, cb) => {
    const safe = file.originalname.replace(/[^a-zA-Z0-9._-]/g, "_");
    cb(null, `${Date.now()}-${safe}`);
  }
});

const upload = multer({
  storage,
  limits: { fileSize: 25 * 1024 * 1024 },
  fileFilter: (_, file, cb) => {
    const allowed = [
      "application/pdf",
      "image/jpeg",
      "image/png",
      "text/plain"
    ];
    cb(null, allowed.includes(file.mimetype));
  }
});

function readDocs() {
  return JSON.parse(fs.readFileSync(DATA_FILE, "utf8"));
}

function writeDocs(docs) {
  fs.writeFileSync(DATA_FILE, JSON.stringify(docs, null, 2));
}

function seed() {
  const docs = readDocs();
  if (docs.length) return;

  const samples = [
    {
      id: crypto.randomUUID(),
      title: "Annihilation of Caste",
      author: "B. R. Ambedkar",
      year: 1936,
      language: "English",
      collection: "Books & Speeches",
      type: "Book",
      description: "A major work by Dr. B. R. Ambedkar examining caste and social reform.",
      tags: ["caste", "social reform", "speech"],
      text: "Annihilation of Caste is a major text by B. R. Ambedkar. This sample record is included for testing the archive search.",
      source: "Sample archival record",
      filename: null,
      createdAt: new Date().toISOString()
    },
    {
      id: crypto.randomUUID(),
      title: "What Congress and Gandhi Have Done to the Untouchables",
      author: "B. R. Ambedkar",
      year: 1945,
      language: "English",
      collection: "Political Writings",
      type: "Book",
      description: "Sample catalog record for testing political writings and archive search.",
      tags: ["politics", "Gandhi", "Congress", "Dalit history"],
      text: "Sample searchable text for What Congress and Gandhi Have Done to the Untouchables.",
      source: "Sample archival record",
      filename: null,
      createdAt: new Date().toISOString()
    },
    {
      id: crypto.randomUUID(),
      title: "Constituent Assembly Debates — Fundamental Rights",
      author: "Constituent Assembly of India",
      year: 1948,
      language: "English",
      collection: "Constituent Assembly Debates",
      type: "Debate",
      description: "Sample record representing a Constituent Assembly debate.",
      tags: ["constitution", "fundamental rights", "assembly"],
      text: "Sample searchable debate text. Replace this record with verified archival material before public release.",
      source: "Sample archival record",
      filename: null,
      createdAt: new Date().toISOString()
    }
  ];

  writeDocs(samples);
}
seed();

app.get("/api/health", (_, res) => {
  res.json({ ok: true, service: "Ambedkar Digital Heritage Archive API" });
});

app.get("/api/stats", (_, res) => {
  const docs = readDocs();
  const languages = new Set(docs.map(d => d.language).filter(Boolean)).size;
  const collections = new Set(docs.map(d => d.collection).filter(Boolean)).size;
  res.json({
    documents: docs.length,
    languages,
    collections,
    digitized: docs.length
  });
});

app.get("/api/documents", (req, res) => {
  let docs = readDocs();
  const q = String(req.query.q || "").trim().toLowerCase();
  const collection = String(req.query.collection || "").trim().toLowerCase();
  const language = String(req.query.language || "").trim().toLowerCase();

  if (q) {
    docs = docs.filter(d =>
      [d.title, d.author, d.description, d.text, d.collection, ...(d.tags || [])]
        .join(" ")
        .toLowerCase()
        .includes(q)
    );
  }

  if (collection) {
    docs = docs.filter(d => String(d.collection).toLowerCase() === collection);
  }

  if (language) {
    docs = docs.filter(d => String(d.language).toLowerCase() === language);
  }

  res.json(docs);
});

app.get("/api/documents/:id", (req, res) => {
  const doc = readDocs().find(d => d.id === req.params.id);
  if (!doc) return res.status(404).json({ error: "Document not found" });
  res.json(doc);
});

app.post("/api/documents", upload.single("file"), (req, res) => {
  const docs = readDocs();
  const body = req.body;

  if (!body.title) {
    if (req.file) fs.unlinkSync(req.file.path);
    return res.status(400).json({ error: "Title is required" });
  }

  const doc = {
    id: crypto.randomUUID(),
    title: body.title,
    author: body.author || "Unknown",
    year: body.year ? Number(body.year) : null,
    language: body.language || "Unknown",
    collection: body.collection || "Uncategorized",
    type: body.type || "Document",
    description: body.description || "",
    tags: body.tags ? body.tags.split(",").map(x => x.trim()).filter(Boolean) : [],
    text: body.text || "",
    source: body.source || "Local upload",
    filename: req.file?.filename || null,
    originalName: req.file?.originalname || null,
    mimeType: req.file?.mimetype || null,
    createdAt: new Date().toISOString()
  };

  docs.unshift(doc);
  writeDocs(docs);
  res.status(201).json(doc);
});

app.delete("/api/documents/:id", (req, res) => {
  const docs = readDocs();
  const doc = docs.find(d => d.id === req.params.id);
  if (!doc) return res.status(404).json({ error: "Document not found" });

  if (doc.filename) {
    const filePath = path.join(UPLOADS, doc.filename);
    if (fs.existsSync(filePath)) fs.unlinkSync(filePath);
  }

  writeDocs(docs.filter(d => d.id !== req.params.id));
  res.json({ ok: true });
});

app.get("/api/collections", (_, res) => {
  const docs = readDocs();
  res.json([...new Set(docs.map(d => d.collection).filter(Boolean))].sort());
});

app.listen(5000, () => {
  console.log("Archive API running at http://localhost:5000");
});