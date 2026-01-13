from app.core.llm import get_llm_loader, generate_response
import sys
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_generation():
    print("Initializing LLM Loader...")
    try:
        loader = get_llm_loader()
        # Force model load
        model = loader.model
        print("Model loaded.")
        
        print("Generating text...")
        response = generate_response("Hello, explain quantum physics in 1 sentence.", max_new_tokens=5)
        print(f"Response: {response}")
        
        if response:
            print("SUCCESS: Generation worked!")
        else:
            print("FAILURE: empty response")
            
    except Exception as e:
        print(f"FAILURE: Exception occurred: {e}")
        import traceback
        with open("verify_error.log", "w") as f:
            traceback.print_exc(file=f)
        sys.exit(1)

if __name__ == "__main__":
    test_generation()
