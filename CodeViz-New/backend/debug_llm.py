
import sys
import os
from pathlib import Path
import torch
import traceback

# Add backend to sys.path
backend_dir = Path(__file__).parent
sys.path.append(str(backend_dir))

from app.core.llm import get_llm_loader

def test_load():
    print(f"CUDA Available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"CUDA Device: {torch.cuda.get_device_name(0)}")
        
    print("Initializing LLM Loader...")
    try:
        loader = get_llm_loader()
        print("Triggering model load...")
        model = loader.model
        print(f"Model loaded: {type(model)}")
        
        print("Testing generation...")
        response = loader.generate("Hi")
        print("Generation response:")
        print(response)
        
    except Exception as e:
        print(f"\nCaught Exception: {type(e).__name__}: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    test_load()
