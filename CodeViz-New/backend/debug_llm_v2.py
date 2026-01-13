
import sys
import os
import traceback

# Add parent directory to path
sys.path.insert(0, os.environ.get("PYTHONPATH", "."))

try:
    from app.core.llm import get_llm_loader
    print("Loading...")
    loader = get_llm_loader()
    print("Generating...")
    loader.generate("test")
    print("Done.")
except:
    with open("error.log", "w", encoding="utf-8") as f:
        traceback.print_exc(file=f)
    print("Error written to error.log")
