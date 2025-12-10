# loader.py
import os
import math
import chromadb
from chromadb.utils import embedding_functions

# -------- CONFIG --------
DATA_PATH = "rag/data"    # folder with your .txt/.html files
CHUNK_SIZE = 1000         # characters for code chunking (tune if needed)
COLLECTION_NAME = "dsa"
# ------------------------

# Initialize Chroma
client = chromadb.PersistentClient(path="chromadb")

embedder = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    embedding_function=embedder
)

LANGUAGE_MAP = {
    ".py": "python", ".c": "c", ".cpp": "cpp", ".js": "javascript", ".html": "html",
    ".css": "css", ".txt": "text", ".md": "markdown", ".java": "java"
}

DATASTRUCTURES = [
    "stack", "queue", "linkedlist", "linked_list", "linked-list",
    "doubly_linkedlist", "singly_linkedlist", "circular_linkedlist",
    "tree", "bst", "binary_search_tree", "heap", "trie", "graph", "hash"
]

def parse_metadata_from_text(text):
    md = {}
    lines = text.splitlines()
    for line in lines[:8]:
        if not line.strip().startswith("###"):
            continue
        t = line.strip().lstrip("#").strip()
        if ":" in t:
            k, v = t.split(":", 1)
            key = k.strip().lower().replace(" ", "_")
            value = v.strip()
            md[key] = value
    return md

def infer_topic_from_filename(filename):
    name = filename.lower()
    for ds in DATASTRUCTURES:
        if ds in name:
            return ds.replace("_", " ").replace("-", " ")
    return "general"

def chunk_text(text, chunk_size):
    if len(text) <= chunk_size:
        return [text]
    chunks = []
    total = len(text)
    n = math.ceil(total / chunk_size)
    for i in range(n):
        start = i * chunk_size
        end = start + chunk_size
        chunk = text[start:end]
        header = f"### CHUNK {i+1}/{n}\n"
        chunks.append(header + chunk)
    return chunks

def load_files():
    loaded_files = 0
    for fname in os.listdir(DATA_PATH):
        full = os.path.join(DATA_PATH, fname)
        if not os.path.isfile(full):
            continue

        _, ext = os.path.splitext(fname)
        ext = ext.lower()

        if ext not in LANGUAGE_MAP and ext not in [".html", ".htm", ".txt"]:
            print(f"Skipping unknown extension: {fname}")
            continue

        with open(full, "r", encoding="utf-8") as f:
            content = f.read()

        header_md = parse_metadata_from_text(content)

        doc_type = header_md.get("document_type", "").strip().lower()
        if not doc_type:
            if ext in [".html", ".htm"] or "<html" in content.lower() or "<!doctype" in content.lower():
                doc_type = "interactive"
            else:
                doc_type = "code"

        topic = header_md.get("topic", "").strip().lower()
        if not topic:
            topic = infer_topic_from_filename(fname)

        language = LANGUAGE_MAP.get(ext, "text")

        metadata_base = {
            "source": fname,
            "type": doc_type,
            "topic": topic,
            "language": language,
            "description": header_md.get("description", "")
        }

        # Remove any existing documents from this source to avoid duplicates (if collection supports it)
        # Note: Chroma python client may have different APIs for delete; for simple runs you can delete DB folder manually.
        # For safety, here we try to delete prior ids if present (best-effort).
        try:
            # build prefix to match previous chunk ids
            existing = collection.get(where={"source": fname}, limit=100)
            if existing and existing.get("ids"):
                # remove by ids if API supports; if not, ignore
                try:
                    collection.delete(ids=existing["ids"])
                    print(f"Removed previous entries for {fname}")
                except Exception:
                    pass
        except Exception:
            pass

        # Interactive: store full content as one document
        if doc_type == "interactive":
            doc_id = f"{fname}::full"
            collection.add(
                ids=[doc_id],
                documents=[content],
                metadatas=[metadata_base]
            )
            print(f"Loaded INTERACTIVE: {fname} as id={doc_id}")
            loaded_files += 1
            continue

        # Code: chunk
        chunks = chunk_text(content, CHUNK_SIZE)
        ids = []
        docs = []
        metas = []
        for idx, chunk in enumerate(chunks):
            doc_id = f"{fname}::chunk::{idx}"
            ids.append(doc_id)
            docs.append(chunk)
            md = metadata_base.copy()
            md.update({"chunk_index": idx, "chunk_count": len(chunks)})
            metas.append(md)

        collection.add(ids=ids, documents=docs, metadatas=metas)
        print(f"Loaded CODE: {fname} chunks={len(chunks)}")
        loaded_files += 1

    print(f"\n✔ Done. Loaded {loaded_files} files into collection '{COLLECTION_NAME}'.")

if __name__ == "__main__":
    if not os.path.exists(DATA_PATH):
        print(f"Data path '{DATA_PATH}' not found. Create the folder and add your files.")
    else:
        load_files()
