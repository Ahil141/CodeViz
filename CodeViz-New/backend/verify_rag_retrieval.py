import sys
import os

# Add backend directory to path
sys.path.append(os.getcwd())

from app.core.rag_pipeline import get_rag_pipeline

def test_rag():
    print("Testing RAG Pipeline...")
    pipeline = get_rag_pipeline()
    
    test_cases = ["Stack", "Queue", "Singly Linked List"]
    
    for name in test_cases:
        print(f"\nQuerying: {name}")
        result = pipeline.get_visualizer(name)
        
        if result["success"]:
            print(f"✅ Found: {result['name']}")
            print(f"   Description: {result['description']}")
            print(f"   Code Length: {len(result['visualizer_code'])} chars")
            if "<!DOCTYPE html>" in result['visualizer_code']:
                 print("   Valid HTML detected.")
            else:
                 print("   ⚠️  WARNING: No HTML tag found.")
        else:
            print(f"❌ Not Found: {result.get('error')}")

if __name__ == "__main__":
    test_rag()
