
import time
import sys
import os

# Add backend directory to path
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "backend"))
sys.path.append(backend_path)

from app.core.llm import get_llm_loader

def test_llm():
    print("--- Starting LLM Verification ---")
    
    # Measure load time
    start_load = time.time()
    try:
        loader = get_llm_loader()
        # Force load
        model = loader.model
        tokenizer = loader.tokenizer
    except Exception as e:
        print(f"FAILED to load model: {e}")
        return
    end_load = time.time()
    
    print(f"Model Load Time: {end_load - start_load:.2f} seconds")
    print(f"Device: {model.device}")
    print(f"Dtype: {model.dtype}")
    
    # Test Generation
    prompt = "Write a python function to reverse a string."
    print(f"\n--- Generating response for prompt: '{prompt}' ---")
    
    start_gen = time.time()
    first_token_time = None
    
    full_response = ""
    token_count = 0
    
    try:
        # We manually use the loader's stream_generate to capture timing
        generator = loader.stream_generate(prompt, max_new_tokens=128)
        
        for token in generator:
            if first_token_time is None:
                first_token_time = time.time()
                print(f"Time to First Token: {first_token_time - start_gen:.2f} seconds")
            
            print(token, end="", flush=True)
            full_response += token
            token_count += 1
            
        end_gen = time.time()
        
        print("\n\n--- Generation Stats ---")
        print(f"Total Tokens: {token_count}")
        print(f"Total Generation Time: {end_gen - start_gen:.2f} seconds")
        if token_count > 0:
            print(f"Tokens per Second: {token_count / (end_gen - first_token_time):.2f}")
        
        # Correctness Checks
        if token_count == 0:
            print("FAILED: No tokens generated.")
        elif token_count >= 256: # Should be capped by our internal limit if passed or default
             print("WARNING: Reached max token limit (check for infinite loop if not expected).")
        else:
             print("SUCCESS: Generation finished naturally.")
             
    except Exception as e:
        print(f"\nFAILED during generation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_llm()
