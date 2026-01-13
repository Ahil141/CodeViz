
import sys
import os
import time

# Add backend directory to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.core.llm import get_llm_loader, LLMSettings

def test_repetition_and_formatting():
    print("Initializing LLM Loader...")
    settings = LLMSettings()
    # Ensure settings match requirements
    settings.model_path = "Qwen/Qwen2.5-Coder-1.5B-Instruct"
    settings.device_map = "auto"
    
    loader = get_llm_loader(settings)
    
    # Force model load
    _ = loader.model
    
    prompt = "what is stack"
    print(f"\nGeneratin response for prompt: '{prompt}'")
    
    start_time = time.time()
    # Use stream_generate to mimic App behavior (raw stream)
    full_response = ""
    print("STREAM OUTPUT:", end=" ", flush=True)
    for chunk in loader.stream_generate(prompt):
        print(chunk, end="", flush=True)
        full_response += chunk
    print("-" * 50)
    print("FINAL RESPONSE:")
    print(full_response)
    print("-" * 50)
    
    end_time = time.time()
    print(f"Time taken: {end_time - start_time:.2f}s")
    
    # Verification checks
    errors = []
    
    # 1. Check for immediate word repetition
    import re
    if re.search(r'\b(\w+)(\s+\1)+\b', full_response, flags=re.IGNORECASE):
        errors.append("FAILED: Immediate word repetition detected (e.g., 'stack stack')")
    else:
        print("PASSED: No immediate word repetition.")
        
    # 2. Check for length
    words = full_response.split()
    if len(words) > 200:
        errors.append(f"WARNING: Response length {len(words)} > 200 words. Might not be concise.")
    else:
        print(f"PASSED: Concise response ({len(words)} words).")
        
    # 3. Check for code block if relevant (stack usually involves code)
    if "```python" in full_response:
        print("PASSED: Python code block detected.")
        # Optional: Check if black formatted (hard to strictly verify without re-running black, but we can look for consistency)
    else:
        print("NOTE: No Python code block detected.")

    if not errors:
        print("\nALL CHECKS PASSED!")
    else:
        print("\nERRORS FOUND:")
        for err in errors:
            print(f"- {err}")

if __name__ == "__main__":
    test_repetition_and_formatting()
