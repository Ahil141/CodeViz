
import time
import sys
import os

print("Starting debug_gen_fast.py")
os.environ["OMP_NUM_THREADS"] = "1"

from app.core.llm import get_llm_loader

loader = get_llm_loader()
print("Model loaded (or lazy load init)")

print("Generating 1 token...")
try:
    start = time.time()
    # Force minimal generation parameters
    response = loader.generate(
        "Hi", 
        max_new_tokens=1, 
        do_sample=False, 
        temperature=None, 
        top_p=None
    )
    elapsed = time.time() - start
    print(f"Generation took {elapsed:.2f}s")
    print(f"Response: '{response}'")
except Exception as e:
    print(f"Generation FAILED: {e}")
    import traceback
    traceback.print_exc()
