
import sys
import os
sys.path.insert(0, os.environ.get("PYTHONPATH", "."))

try:
    import transformers
    print(f"Transformers version: {transformers.__version__}")
    
    try:
        from transformers.utils import LossKwargs
        print("LossKwargs found in transformers.utils")
    except ImportError:
        print("LossKwargs NOT found in transformers.utils")
        
    # Search for it
    import transformers.utils as utils
    print(f"Utils dir: {dir(utils)}")

except Exception as e:
    print(e)
