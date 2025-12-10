import chromadb

# Connect to your persistent Chroma DB
client = chromadb.PersistentClient(path="chromadb")

# Load collection
collection = client.get_collection("dsa")

print("Running test retrieval...\n")

# Query the vector DB using text similarity
results = collection.query(
    query_texts=["give code for stack"],
    n_results=1
)

# Print the raw result for debugging
print("Raw result from DB:", results, "\n")

# Extract the retrieved document
if results["documents"] and len(results["documents"][0]) > 0:
    doc = results["documents"][0][0]
    print("Retrieved document:\n")
    print(doc)
else:
    print("❌ No document retrieved!")
