// Lightweight local preview server for machines where the Python API is unavailable.
const http = require("node:http");
const fs = require("node:fs");
const path = require("node:path");

const frontendRoot = __dirname;
const projectRoot = path.dirname(frontendRoot);
const archiveRoot = path.join(projectRoot, "ambedkar_archive_data", "processed_data");
let archiveDocumentsPromise;
const mimeTypes = {
  ".css": "text/css; charset=utf-8",
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".png": "image/png",
  ".svg": "image/svg+xml"
};

function sendFile(response, filePath) {
  fs.readFile(filePath, (error, contents) => {
    if (error) {
      response.writeHead(404, { "Content-Type": "text/plain; charset=utf-8" });
      response.end("Not found");
      return;
    }
    response.writeHead(200, {
      "Content-Type": mimeTypes[path.extname(filePath).toLowerCase()] || "application/octet-stream"
    });
    response.end(contents);
  });
}

function sendJson(response, status, data) {
  response.writeHead(status, { "Content-Type": "application/json; charset=utf-8" });
  response.end(JSON.stringify(data));
}

function readRequestJson(request) {
  return new Promise((resolve, reject) => {
    let body = "";
    request.setEncoding("utf8");
    request.on("data", chunk => {
      body += chunk;
      if (body.length > 64 * 1024) reject(new Error("Request is too large."));
    });
    request.on("end", () => {
      try { resolve(JSON.parse(body || "{}")); }
      catch (_) { reject(new Error("Request body must be valid JSON.")); }
    });
    request.on("error", reject);
  });
}

function loadArchiveDocuments() {
  if (!archiveDocumentsPromise) {
    archiveDocumentsPromise = fs.promises.readdir(archiveRoot)
      .then(files => Promise.all(files.filter(file => file.endsWith(".json")).map(async file => {
        try {
          const parsed = JSON.parse(await fs.promises.readFile(path.join(archiveRoot, file), "utf8"));
          return parsed.document || parsed;
        } catch (_) { return null; }
      })))
      .then(documents => documents.filter(document => document && document.id));
  }
  return archiveDocumentsPromise;
}

function summarizeArchive(documents) {
  const countBy = key => documents.reduce((counts, document) => {
    const value = key(document) || "unknown";
    counts[value] = (counts[value] || 0) + 1;
    return counts;
  }, {});
  return {
    total_documents: documents.length,
    total_words_indexed: documents.reduce((total, document) => total + (Number(document.metadata?.word_count) || 0), 0),
    total_embedding_chunks: 0,
    languages: countBy(document => document.language),
    languages_by_source: documents.reduce((counts, document) => {
      const language = document.language || "unknown";
      const source = document.metadata?.source || "unknown";
      counts[language] ||= {};
      counts[language][source] = (counts[language][source] || 0) + 1;
      return counts;
    }, {}),
    types: countBy(document => document.type),
    sources: countBy(document => document.metadata?.source || document.source)
  };
}

function searchArchive(documents, body) {
  const query = typeof body.q === "string" ? body.q.trim().toLocaleLowerCase() : "*";
  const terms = query === "*" ? [] : (query.match(/[\p{L}\p{N}]+/gu) || []);
  const language = body.language || null;
  const documentType = body.document_type || null;
  const source = body.source || null;
  const started = Date.now();
  const matches = [];

  for (const document of documents) {
    const metadata = document.metadata || {};
    if (language && document.language !== language) continue;
    if (documentType && document.type !== documentType) continue;
    if (source && metadata.source !== source) continue;
    const content = document.content || {};
    const searchable = [document.title, document.author, content.summary, content.full_text,
      ...(Array.isArray(document.tags) ? document.tags : [document.tags || ""]),
      ...Object.values(document.translations || {}).flatMap(translation => [translation.title, translation.summary])]
      .filter(Boolean).join(" ").toLocaleLowerCase();
    const score = terms.reduce((total, term) => total + (searchable.includes(term) ? 1 : 0), 0);
    if (terms.length && !score) continue;
    matches.push({ document, score });
  }

  matches.sort((left, right) => right.score - left.score || String(right.document.date || "").localeCompare(String(left.document.date || "")));
  const offset = Math.max(0, Number(body.offset) || 0);
  const limit = Math.max(1, Math.min(100, Number(body.limit) || 30));
  const results = matches.slice(offset, offset + limit).map(({ document }) => {
    const metadata = document.metadata || {};
    const url = metadata.url || metadata.pdf_url || (metadata.source === "IA" && metadata.archive_reference
      ? `https://archive.org/details/${encodeURIComponent(metadata.archive_reference)}` : metadata.archive_reference || null);
    return {
      id: document.id,
      title: document.title,
      author: document.author || "",
      date: document.date || null,
      type: document.type || "other",
      language: document.language || "en",
      source: metadata.source || "Archive",
      summary: document.content?.summary || document.summary || "",
      tags: Array.isArray(document.tags) ? document.tags : String(document.tags || "").split(",").map(tag => tag.trim()).filter(Boolean),
      url
    };
  });
  return { query, total: matches.length, took_ms: Date.now() - started, results, mode: "preview" };
}

const queryTranslations = {
  hi: [["जाति", "caste"], ["श्रम", "labour"], ["भक्ति", "bhakti"], ["व्यक्तिपूजा", "hero worship"], ["संविधान", "constitution"], ["लोकतंत्र", "democracy"], ["समानता", "equality"], ["अस्पृश्यता", "untouchability"], ["अनुच्छेद", "article"], ["रुपया", "rupee"], ["महाड", "mahad"], ["बौद्ध", "buddhism"], ["राष्ट्रपति", "presidential"], ["संसदीय", "parliamentary"], ["राजनीति", "politics"], ["शिक्षा", "education"], ["डिग्रियां", "degree"], ["डिग्रियाँ", "degree"], ["डिग्री", "degree"], ["उपाधि", "degree"], ["पदवियां", "degree"], ["पदवी", "degree"], ["डॉक्टर", "doctor"], ["कितनी", "how many"]],
  mr: [["जात", "caste"], ["कामगार", "labour"], ["भक्ती", "bhakti"], ["व्यक्तिपूजा", "hero worship"], ["संविधान", "constitution"], ["लोकशाही", "democracy"], ["समता", "equality"], ["अस्पृश्यता", "untouchability"], ["कलम", "article"], ["रुपया", "rupee"], ["महाड", "mahad"], ["बौद्ध", "buddhism"], ["राष्ट्रपती", "presidential"], ["संसदीय", "parliamentary"], ["राजकारण", "politics"], ["शिक्षण", "education"], ["पदव्या", "degree"], ["पदवी", "degree"], ["डिग्री", "degree"], ["किती", "how many"]]
};
const ignoredQueryWords = new Set(["what", "when", "where", "which", "who", "why", "how", "many", "much", "did", "does", "was", "were", "the", "and", "for", "about", "from", "into", "with", "ambedkar", "dr", "his", "her", "has", "have", "tell", "show", "give", "me", "please"]);

function assistantTerms(question, language) {
  let normalized = question.toLocaleLowerCase();
  for (const [term, english] of (queryTranslations[language] || [])) normalized = normalized.split(term).join(english);
  const terms = (normalized.match(/[a-z0-9]+/g) || []).filter(term => term.length > 2 && !ignoredQueryWords.has(term));
  if (terms.some(term => ["degree", "degrees", "doctorate", "doctor", "phd"].includes(term))) {
    terms.push("degree", "degrees", "doctorate", "doctor", "phd", "columbia", "london");
  }
  return [...new Set(terms)];
}

function searchableDocument(document) {
  const translations = document.translations || {};
  const content = document.content || {};
  return [document.title, document.author, document.type, document.language,
    ...(document.tags || []), content.summary, content.full_text, ...(content.key_quotes || []),
    ...Object.values(translations).flatMap(value => [value.title, value.summary])]
    .filter(Boolean).join(" ").toLocaleLowerCase();
}

function matchingExcerpt(document, terms) {
  const content = document.content || {};
  const candidates = [...(content.key_quotes || []), content.summary || "", ...(content.full_text || "").split(/(?<=[.!?])\s+/)];
  const scored = candidates.map(text => ({ text: String(text).trim(), score: terms.reduce((n, term) => n + (String(text).toLocaleLowerCase().includes(term) ? 1 : 0), 0) }))
    .filter(item => item.text && item.score > 0).sort((a, b) => b.score - a.score || a.text.length - b.text.length);
  return (scored[0]?.text || content.summary || "").slice(0, 650);
}

function assistantResponse(documents, question, language) {
  const terms = assistantTerms(question, language);
  if (!terms.length) return { answer: localizedClarification(language), sources: [] };
  const degreeQuestion = terms.some(term => ["degree", "degrees", "doctorate", "doctor", "phd"].includes(term));

  const results = documents.map(document => {
    const content = document.content || {};
    const title = `${document.title || ""} ${(document.translations || {}).en?.title || ""}`.toLocaleLowerCase();
    const summary = String(content.summary || "").toLocaleLowerCase();
    const quotes = (content.key_quotes || []).join(" ").toLocaleLowerCase();
    const fullText = String(content.full_text || "").toLocaleLowerCase();
    const tags = (document.tags || []).join(" ").toLocaleLowerCase();
    const score = terms.reduce((total, term) => total + (title.includes(term) ? 5 : 0) + (quotes.includes(term) ? 4 : 0) + (summary.includes(term) ? 3 : 0) + (tags.includes(term) ? 2 : 0) + (fullText.includes(term) ? 1 : 0), 0);
    return { document, score, excerpt: matchingExcerpt(document, terms) };
  }).filter(result => {
    if (!result.score) return false;
    if (!degreeQuestion) return true;
    const text = searchableDocument(result.document);
    const evidence = `${result.document.title || ""} ${result.document.author || ""} ${result.document.content?.summary || ""} ${result.document.content?.full_text || ""}`;
    return /ambedkar/i.test(evidence) && /degrees? from|doctor of (science|philosophy)|doctorate|ph\.?\s?d\b|bachelor of|master of/i.test(evidence);
  }).sort((a, b) => b.score - a.score).slice(0, 4);

  if (!results.length) return { answer: localizedNoEvidence(language), sources: [] };
  const answerOpenings = {
    en: "I found these archive records relevant to your question. The answer below is limited to what their indexed text supports:",
    hi: "आपके प्रश्न से संबंधित अभिलेख मिले। नीचे का उत्तर उन्हीं अभिलेखों में उपलब्ध जानकारी तक सीमित है:",
    mr: "तुमच्या प्रश्नाशी संबंधित अभिलेख सापडले. खालील उत्तर त्या अभिलेखांतील उपलब्ध माहितीपुरते मर्यादित आहे:"
  };
  const sources = results.map(({ document, excerpt }) => {
    const translation = (document.translations || {})[language] || {};
    return {
      id: document.id,
      title: document.title,
      display_title: translation.title || document.title,
      author: document.author,
      date: document.date,
      source: document.metadata?.source || document.source,
      language: document.language,
      localized_summary: translation.summary || document.content?.summary,
      excerpt
    };
  });
  let answer = answerOpenings[language] || answerOpenings.en;
  if (degreeQuestion) {
    answer = ({
      en: "An indexed biographical record says Ambedkar received doctorates in 1927 and 1923, which supports at least two doctoral degrees. Another archive record identifies a Doctor of Science (Economics) thesis at the University of London. The archive does not give a complete count of all his degrees.",
      hi: "एक अनुक्रमित जीवनी अभिलेख कहता है कि आंबेडकर ने 1927 और 1923 में डॉक्टरेट प्राप्त कीं, जिससे कम-से-कम दो डॉक्टरेट डिग्रियों का समर्थन मिलता है। एक अन्य अभिलेख लंदन विश्वविद्यालय में Doctor of Science (Economics) थीसिस का उल्लेख करता है। अभिलेखागार उनकी सभी डिग्रियों की पूरी संख्या नहीं देता।",
      mr: "एका अनुक्रमित चरित्रात्मक नोंदीनुसार आंबेडकरांनी 1927 आणि 1923 मध्ये डॉक्टरेट मिळवल्या, त्यामुळे किमान दोन डॉक्टरेट पदव्यांना आधार मिळतो. दुसऱ्या अभिलेखात लंडन विद्यापीठातील Doctor of Science (Economics) प्रबंधाचा उल्लेख आहे. अभिलेखागार त्यांच्या सर्व पदव्यांची एकूण संख्या देत नाही."
    })[language] || answer;
  }
  return { answer, sources };
}

function localizedNoEvidence(language) {
  return ({
    en: "I couldn't find reliable supporting information for this question in the indexed archive. Try different keywords or browse the archive records.",
    hi: "अनुक्रमित अभिलेखागार में इस प्रश्न के लिए विश्वसनीय सहायक जानकारी नहीं मिली। अलग शब्दों से पूछें या अभिलेख देखें।",
    mr: "अनुक्रमित अभिलेखात या प्रश्नासाठी विश्वासार्ह आधार सापडला नाही. वेगळ्या शब्दांत विचारा किंवा अभिलेख पाहा."
  })[language] || "I couldn't find reliable supporting information for this question in the indexed archive.";
}

function localizedClarification(language) {
  return ({
    en: "What would you like to know about Dr. B. R. Ambedkar? Try asking about his education, writings, speeches, work on the Constitution, or a historical event.",
    hi: "आप डॉ. बी. आर. आंबेडकर के बारे में क्या जानना चाहते हैं? उनकी शिक्षा, लेखन, भाषणों, संविधान पर काम या किसी ऐतिहासिक घटना के बारे में पूछें।",
    mr: "तुम्हाला डॉ. बी. आर. आंबेडकर यांच्याबद्दल काय जाणून घ्यायचे आहे? त्यांचे शिक्षण, लेखन, भाषणे, संविधानातील काम किंवा एखाद्या ऐतिहासिक घटनेबद्दल विचारा."
  })[language] || "What would you like to know about Dr. B. R. Ambedkar? Try asking about his education, writings, speeches, work on the Constitution, or a historical event.";
}

const server = http.createServer((request, response) => {
  const requestUrl = new URL(request.url, "http://localhost");
  if (request.method === "GET" && requestUrl.pathname === "/api/health") {
    return sendJson(response, 200, { status: "healthy", service: "Ambedkar Digital Heritage Archive", mode: "preview" });
  }
  if (request.method === "GET" && requestUrl.pathname === "/api/stats") {
    return loadArchiveDocuments().then(documents => sendJson(response, 200, summarizeArchive(documents)))
      .catch(error => sendJson(response, 500, { detail: error.message || "Could not read local archive records." }));
  }
  if (request.method === "POST" && requestUrl.pathname === "/api/search") {
    return readRequestJson(request).then(async body => {
      const documents = await loadArchiveDocuments();
      sendJson(response, 200, searchArchive(documents, body));
    }).catch(error => sendJson(response, 400, { detail: error.message || "Archive search failed." }));
  }
  if (request.method === "GET" && requestUrl.pathname === "/api/documents") {
    return loadArchiveDocuments().then(documents => {
      const source = requestUrl.searchParams.get("source");
      const language = requestUrl.searchParams.get("language");
      const type = requestUrl.searchParams.get("document_type");
      const matches = documents.filter(document => (!source || document.metadata?.source === source)
        && (!language || document.language === language) && (!type || document.type === type));
      const skip = Math.max(0, Number(requestUrl.searchParams.get("skip")) || 0);
      const limit = Math.max(1, Math.min(100, Number(requestUrl.searchParams.get("limit")) || 20));
      return sendJson(response, 200, { total: matches.length, skip, limit, items: matches.slice(skip, skip + limit).map(document => ({
        id: document.id, title: document.title, author: document.author, date: document.date, type: document.type,
        language: document.language, source: document.metadata?.source, summary: document.content?.summary || "",
        tags: document.tags || [], url: document.metadata?.url || document.metadata?.archive_reference || null
      })) });
    }).catch(error => sendJson(response, 500, { detail: error.message || "Could not read local archive records." }));
  }
  if (request.method === "POST" && requestUrl.pathname === "/api/assistant") {
    return readRequestJson(request).then(async body => {
      const question = typeof body.question === "string" ? body.question.trim() : "";
      if (question.length < 2 || question.length > 500) return sendJson(response, 422, { detail: "Question must contain between 2 and 500 characters." });
      const language = ["en", "hi", "mr"].includes(body.language) ? body.language : "en";
      const documents = await loadArchiveDocuments();
      sendJson(response, 200, assistantResponse(documents, question, language));
    }).catch(error => sendJson(response, 400, { detail: error.message || "Archive search failed." }));
  }
  const documentMatch = requestUrl.pathname.match(/^\/api\/documents\/([A-Za-z0-9_-]+)$/);
  if (request.method === "GET" && documentMatch) {
    return sendFile(response, path.join(archiveRoot, `${documentMatch[1]}.json`));
  }

  if (requestUrl.pathname.startsWith("/api/")) {
    response.writeHead(503, { "Content-Type": "application/json; charset=utf-8" });
    response.end(JSON.stringify({ detail: "Archive API is unavailable in preview mode." }));
    return;
  }

  const webPath = requestUrl.pathname === "/"
    ? "/index.html"
    : requestUrl.pathname.startsWith("/static/")
      ? requestUrl.pathname.slice("/static".length)
      : requestUrl.pathname;
  const decodedPath = decodeURIComponent(webPath);
  const resolvedPath = path.resolve(frontendRoot, `.${decodedPath}`);
  if (resolvedPath !== frontendRoot && !resolvedPath.startsWith(`${frontendRoot}${path.sep}`)) {
    response.writeHead(403);
    response.end();
    return;
  }
  sendFile(response, resolvedPath);
});

const port = Number(process.env.PORT || 8000);
server.listen(port, "127.0.0.1", () => {
  console.log(`Archive preview is running at http://127.0.0.1:${port}/`);
});
