
import os
import sys
# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.core.llm import get_llm_loader

print("Initializing LLM Loader...")
loader = get_llm_loader()

print("Generating text...")
try:
    response = loader.generate("Hello, how are you?", max_new_tokens=20)
    print(f"Response: {response}")
except Exception as e:
    print(f"Error: {e}")
