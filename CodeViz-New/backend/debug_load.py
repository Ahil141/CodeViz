
import time
import sys
import os

print("Starting debug_load.py")

# Set env var to potentially fix hanging
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

try:
    from app.core.llm import get_llm_loader
    print("Import successful")
    
    loader = get_llm_loader()
    print(f"Settings: {loader.settings.model_path}")
    
    print("Accessing loader.model (triggers lazy load)...")
    start = time.time()
    model = loader.model
    elapsed = time.time() - start
    print(f"Model loaded in {elapsed:.2f}s")
    
    print("Accessing loader.tokenizer...")
    tokenizer = loader.tokenizer
    print("Tokenizer loaded")
    
except Exception as e:
    print(f"FAILED: {e}")
    import traceback
    traceback.print_exc()
