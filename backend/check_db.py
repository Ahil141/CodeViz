import chromadb

# Connect to your persistent Chroma DB
client = chromadb.PersistentClient(path="chromadb")

# Load collection
collection = client.get_collection("dsa")

# Print everything stored in DB
data = collection.get()

print("\n=== COLLECTION CONTENTS ===")
print("IDs:", data.get("ids"))
print("\nDocuments:", data.get("documents"))
print("\nMetadatas:", data.get("metadatas"))
print("\nEmbeddings Count:", len(data.get("embeddings", [])))
