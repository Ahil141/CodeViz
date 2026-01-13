import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add backend to path
backend_dir = Path(__file__).parent / "backend"
sys.path.append(str(backend_dir))

# Mock torch and transformers to avoid large imports and GPU checks in this environment
with patch.dict('sys.modules', {
    'torch': MagicMock(),
    'transformers': MagicMock(),
    'huggingface_hub': MagicMock(),
}):
    # Import after mocking
    from app.core.llm import LLMLoader, LLMSettings
    
    print("Successfully imported LLMLoader.")
    
    # Check if stream_generate has the new parameters in source code check or just basic import check
    # We can inspect the code dynamically or just rely on the import not failing.
    # Since we modified the code, reading it via this script is also a way.
    
    loader = LLMLoader()
    print("LLMLoader initialized.")

print("Verification script finished.")
