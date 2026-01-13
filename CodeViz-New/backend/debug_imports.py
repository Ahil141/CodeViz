
import time
import sys
import os

print("Starting debug_imports.py")

def measure_import(module_name):
    start = time.time()
    print(f"Importing {module_name}...", end="", flush=True)
    try:
        __import__(module_name)
        elapsed = time.time() - start
        print(f" Done ({elapsed:.2f}s)")
    except Exception as e:
        print(f" FAILED: {e}")

measure_import("sys")
measure_import("os")
measure_import("pydantic")
measure_import("pydantic_settings")
measure_import("dotenv")

# Torch often takes a while
measure_import("torch")

# Transformers often takes a while
measure_import("transformers")

print("Now importing app.core.llm...")
start = time.time()
try:
    from app.core.llm import get_llm_loader
    elapsed = time.time() - start
    print(f"Import app.core.llm Done ({elapsed:.2f}s)")
except Exception as e:
    print(f"Import app.core.llm FAILED: {e}")

print("Debug imports finished.")
