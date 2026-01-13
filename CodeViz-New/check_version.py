import transformers
from transformers.cache_utils import DynamicCache
import sys

print(f"Transformers version: {transformers.__version__}")
try:
    c = DynamicCache()
    print("DynamicCache methods/attributes:")
    print(dir(c))
    
    if hasattr(c, 'get_seq_length'):
        print("get_seq_length found.")
    else:
        print("get_seq_length NOT found.")
        
    if hasattr(c, 'seen_tokens'):
        print("seen_tokens found.")
    else:
        print("seen_tokens NOT found.")

except Exception as e:
    print(f"Error inspecting DynamicCache: {e}")
