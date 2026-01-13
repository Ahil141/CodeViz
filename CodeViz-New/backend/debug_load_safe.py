
import time
import sys
import os
import traceback

log_file = "debug_load_safe.log"

def log(msg):
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(msg + "\n")
    print(msg, flush=True)

# Clear log
with open(log_file, "w") as f:
    f.write("Starting debug_load_safe.py\n")

try:
    log("Importing app.core.llm...")
    from app.core.llm import get_llm_loader
    log("Import successful")
    
    loader = get_llm_loader()
    log(f"Model path: {loader.settings.model_path}")
    
    log("Loading tokenizer...")
    tokenizer = loader.tokenizer
    log("Tokenizer loaded.")
    
    log("Loading model...")
    model = loader.model
    log("Model loaded successfully.")
    
except Exception as e:
    log(f"CRITICAL EXCEPTION: {e}")
    with open(log_file, "a") as f:
        traceback.print_exc(file=f)
    sys.exit(1)
