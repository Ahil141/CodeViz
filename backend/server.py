# server.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import chromadb
from llm.deepseek_client import generate  # your LLM client - keep this as-is

app = Flask(__name__)
CORS(app)

client = chromadb.PersistentClient(path="chromadb")
collection = client.get_collection("dsa")

INTERACTIVE_KEYWORDS = [
    "interactive", "visual", "visualize", "visualise", "demo", "show",
    "working", "illustrate", "illustration", "walkthrough", "play", "teach",
    "help me learn", "explain visually"
]

def wants_interactive(query_text: str) -> bool:
    q = query_text.lower()
    return any(k in q for k in INTERACTIVE_KEYWORDS)

@app.route("/ask", methods=["POST"])
def ask():
    payload = request.json or {}
    query = payload.get("query", "").strip()
    if not query:
        return jsonify({"error": "Empty query"}), 400

    prefer_interactive = wants_interactive(query)

    results = None
    try:
        if prefer_interactive:
            # try interactive first
            results = collection.query(query_texts=[query], n_results=1, where={"type": "interactive"})
            # fallback
            if not results.get("documents") or not results["documents"][0]:
                results = collection.query(query_texts=[query], n_results=1)
        else:
            # prefer code results
            results = collection.query(query_texts=[query], n_results=3, where={"type": "code"})
            # if nothing found, fallback to any
            if not results.get("documents") or not results["documents"][0]:
                results = collection.query(query_texts=[query], n_results=3)
    except Exception as e:
        print("Chroma query failed:", e)
        results = collection.query(query_texts=[query], n_results=3)

    # Parse result: find best doc and metadata
    doc = ""
    metadata = {}
    try:
        docs = results.get("documents", [])
        metas = results.get("metadatas", [])
        # handle empty results
        if docs and docs[0]:
            doc = docs[0][0]
        if metas and metas[0]:
            metadata = metas[0][0] or {}
    except Exception:
        doc = ""
        metadata = {}

    doc_type = metadata.get("type", metadata.get("document_type", "code"))

    # If interactive, return the HTML directly
    if doc and doc_type == "interactive":
        return jsonify({
            "type": "interactive",
            "html": doc,
            "metadata": metadata,
            "message": "Interactive HTML returned."
        })

    # For code: we want the full file, not a single chunk.
    # Strategy:
    # 1) If initial result's metadata has `source`, use it. Otherwise try to extract from returned doc id in results (if available).
    # 2) Query all documents with where={"source": source} and type=code (n_results large)
    # 3) Sort by chunk_index metadata and join.
    code_full = ""
    source_name = metadata.get("source") or metadata.get("source_name") or ""

    # If initial query returned multiple results, try to identify the most common source among top results
    try:
        # collect candidate sources from returned metadatas
        candidate_sources = []
        metas_list = metas[0] if metas and metas[0] else []
        for m in metas_list:
            if isinstance(m, dict) and m.get("source"):
                candidate_sources.append(m.get("source"))
        if candidate_sources and not source_name:
            # pick most frequent
            from collections import Counter
            c = Counter(candidate_sources)
            most_common = c.most_common(1)
            if most_common:
                source_name = most_common[0][0]
    except Exception:
        pass

    # If we got a candidate source, fetch all chunks for that source
    if source_name:
        try:
            # fetch many results that match source (and type code) - n_results should be large enough to contain all chunks
            r = collection.query(query_texts=[query], n_results=100, where={"source": source_name})
            docs_r = r.get("documents", [])
            metas_r = r.get("metadatas", [])
            fetched = []
            if docs_r and metas_r and docs_r[0]:
                # docs_r[0] is a list of doc strings; metas_r[0] is a list of metadata dicts
                for d, md in zip(docs_r[0], metas_r[0]):
                    fetched.append((md.get("chunk_index", 0), d, md))
                # sort by chunk_index (ensure int)
                fetched_sorted = sorted(fetched, key=lambda x: int(x[0]) if x and x[0] is not None else 0)
                parts = []
                for idx, dtext, md in fetched_sorted:
                    # remove chunk header if present
                    if isinstance(dtext, str) and dtext.startswith("### CHUNK"):
                        # remove first newline after header line
                        parts.append("\n".join(dtext.splitlines()[1:]))
                    else:
                        parts.append(dtext)
                code_full = "\n".join(parts).strip()
        except Exception as e:
            print("Failed to fetch all chunks by source:", e)
            code_full = doc or ""

    # If we still don't have assembled code, fallback: if the initial doc looks like a chunked piece, try to reconstruct from top-N results
    if not code_full:
        try:
            # flatten returned docs list
            collected = []
            if docs and docs[0]:
                for i, d in enumerate(docs[0]):
                    md = metas[0][i] if metas and metas[0] and len(metas[0]) > i else {}
                    idx = md.get("chunk_index", i)
                    collected.append((int(idx) if isinstance(idx, int) or (isinstance(idx, str) and idx.isdigit()) else i, d))
            if collected:
                collected_sorted = sorted(collected, key=lambda x: x[0])
                code_full = "\n".join([c[1] if not (isinstance(c[1], str) and c[1].startswith("### CHUNK")) else "\n".join(c[1].splitlines()[1:]) for c in collected_sorted]).strip()
        except Exception:
            code_full = doc or ""

    # Final fallback
    if not code_full:
        code_full = doc or ""

    # Ask LLM for explanation/augmentation
    explanation = ""
    try:
        explanation = generate(query) if query else ""
    except Exception as e:
        print("LLM generate failed:", e)
        explanation = ""

    return jsonify({
        "type": "code",
        "code": code_full,
        "explanation": explanation,
        "metadata": {"source": source_name, **metadata} if metadata else {"source": source_name},
        "message": "Code + explanation returned (reassembled)."
    })

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
