import sys
import os

# Add backend to path
sys.path.append(os.getcwd())

from app.db.chroma_store import get_chroma_store

def check_db_content():
    store = get_chroma_store()
    try:
        # Query for all interactive types
        # Note: metadata filtering with empty query might not work exactly as 'get all' in some versions,
        # but let's try to just use count or a broad query.
        
        # 1. Get total count
        count = store.count()
        print(f"Total documents in DB: {count}")
        
        # 2. Peek to see types (or just query for type=interactive)
        results = store.collection.get(where={"type": "interactive"})
        
        ids = results['ids']
        print(f"Interactive documents found: {len(ids)}")
        print("-" * 20)
        for doc_id in ids:
            print(f"- {doc_id}")
            
    except Exception as e:
        print(f"Error checking DB: {e}")

if __name__ == "__main__":
    check_db_content()
