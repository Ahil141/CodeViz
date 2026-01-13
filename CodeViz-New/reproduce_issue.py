
import sys
import os
from pathlib import Path

# Add backend to path
backend_path = Path("backend").resolve()
sys.path.append(str(backend_path))

from app.core.llm import get_llm_loader
from app.utils.prompts import format_general_prompt, format_ds_tutor_prompt

def test_generation():
    print("Initializing LLM Loader...")
    loader = get_llm_loader()
    
    # Test case from user report
    print("\n--- Testing 'stack' query ---")
    query = "What is a stack?"
    
    # Use the DS prompt as that's likely what they used
    prompt = format_ds_tutor_prompt("Stack", query)
    print(f"Prompt type: {type(prompt)}")
    sys.stdout.flush()
    try:
        if isinstance(prompt, list):
            print(f"Prompt preview: {prompt}")
        else:
            print(f"Prompt preview:\n{prompt[:200]}...")
        sys.stdout.flush()
        
        print("\nGenerating...")
        sys.stdout.flush()
        # Using the same parameters as in chat.py
        response = loader.generate(prompt, max_new_tokens=128)
        
        print("\nResponse:")
        print(response)
        sys.stdout.flush()
    except Exception as e:
        print(f"\nERROR during generation: {e}")
        import traceback
        traceback.print_exc()
        sys.stdout.flush()

if __name__ == "__main__":
    test_generation()
