import chromadb

# Persistent ChromaDB client (same folder used in loader.py)
client = chromadb.PersistentClient(path="chromadb")

# Load the DS collection
collection = client.get_collection("dsa")

def search(query):
    """
    Perform semantic search in ChromaDB.
    Returns the best matching document (code snippet).
    """
    results = collection.query(
        query_texts=[query],
        n_results=1
    )

    if results["documents"]:
        return results["documents"][0][0]

    return "No matching code found."
