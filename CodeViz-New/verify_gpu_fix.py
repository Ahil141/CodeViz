import sys
import os
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent / "backend"
sys.path.append(str(backend_dir))

from app.core.llm import get_llm_loader

def verify_gpu():
    print("Starting verification...")
    try:
        loader = get_llm_loader()
        # Trigger loading
        model = loader.model
        print(f"Verification Script - Model Device: {model.device}")
        
        import torch
        if torch.cuda.is_available():
            print(f"CUDA Available: {torch.cuda.is_available()}")
            print(f"Current Device: {torch.cuda.current_device()}")
            print(f"Device Name: {torch.cuda.get_device_name(0)}")
            
            if "cuda" in str(model.device):
                print("SUCCESS: Model is on GPU.")
            else:
                print("FAILURE: Model is NOT on GPU.")
        else:
            print("WARNING: CUDA not available in this environment.")
            
    except Exception as e:
        print(f"Verification Failed with error: {e}")

if __name__ == "__main__":
    verify_gpu()
