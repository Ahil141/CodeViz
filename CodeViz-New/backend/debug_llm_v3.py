
import sys
import os
import traceback
import torch

# Add parent directory to path
sys.path.insert(0, os.environ.get("PYTHONPATH", "."))

log_file = "error_v3.log"

def log(msg):
    print(msg)
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(msg + "\n")

try:
    # Clear previous log
    with open(log_file, "w", encoding="utf-8") as f:
        f.write("Starting debug session v3\n")

    log(f"Python version: {sys.version}")
    log(f"Torch version: {torch.__version__}")
    log(f"CUDA available: {torch.cuda.is_available()}")
    
    from app.core.llm import get_llm_loader
    
    log("Import successful. getting loader...")
    loader = get_llm_loader()
    
    log(f"Model path from settings: {loader.settings.model_path}")
    log(f"Device map from settings: {loader.settings.device_map}")
    
    log("Attempting generation...")
    response = loader.generate("Test prompt")
    log(f"Generation successful. Response length: {len(response)}")
    log(f"Response: {response}")

except Exception as e:
    log("\n!!! EXCEPTION CAUGHT !!!")
    log(str(e))
    with open(log_file, "a", encoding="utf-8") as f:
        traceback.print_exc(file=f)
    print("Full traceback written to error_v3.log")
