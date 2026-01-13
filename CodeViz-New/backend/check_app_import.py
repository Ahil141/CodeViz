import sys
import os
from pathlib import Path

# Add backend to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    print("Attempting to import app.main...")
    from app.main import app
    print("Success: app.main imported.")
except Exception as e:
    print(f"Error importing app.main: {e}")
    sys.exit(1)
