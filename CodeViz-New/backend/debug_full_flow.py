
import time
import sys
import os

print("Starting debug_full_flow.py")
# Add parent to path if needed (already handled by cwd usually)
sys.path.insert(0, os.getcwd())

try:
    from app.core.llm import get_llm_loader
    
    loader = get_llm_loader()
    print("Loader initialized.")
    
    prompt = "Hello, tell me a joke."
    print(f"Generating for prompt: '{prompt}'")
    
    start = time.time()
    response = loader.generate(
        prompt,
        max_new_tokens=64, # Small enough to be fast, large enough to verify content
        do_sample=False,
        temperature=0.7 # Should be ignored if do_sample=False
    )
    elapsed = time.time() - start
    
    print(f"Generation successful in {elapsed:.2f}s")
    print("-" * 20)
    print(response)
    print("-" * 20)
    
except Exception as e:
    print(f"FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
