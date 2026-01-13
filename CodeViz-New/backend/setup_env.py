"""
Helper script to create .env file for CodeLearn AI backend.
Run this script to set up your environment variables.
"""

import os
from pathlib import Path

def create_env_file():
    """Create .env file with template."""
    backend_dir = Path(__file__).parent
    env_file = backend_dir / ".env"
    
    if env_file.exists():
        print(f".env file already exists at: {env_file}")
        response = input("Do you want to overwrite it? (y/n): ")
        if response.lower() != 'y':
            print("Keeping existing .env file.")
            return
    
    print("\n" + "="*60)
    print("CodeLearn AI - Environment Setup")
    print("="*60)
    print("\nThis script will help you create a .env file.")
    print("You'll need a HuggingFace token to use LLaMA models.")
    print("\nSteps:")
    print("1. Get a token from: https://huggingface.co/settings/tokens")
    print("2. Accept model access at: https://huggingface.co/meta-llama/Meta-Llama-3-8B")
    print("\n" + "-"*60)
    
    hf_token = input("\nEnter your HuggingFace token (or press Enter to skip): ").strip()
    
    env_content = f"""# HuggingFace Token (Required for LLaMA models)
# Get your token from: https://huggingface.co/settings/tokens
# Accept model access at: https://huggingface.co/meta-llama/Meta-Llama-3-8B
HUGGINGFACE_TOKEN={hf_token if hf_token else 'your_token_here'}

# LLM Configuration
LLM_MODEL_PATH=meta-llama/Meta-Llama-3-8B
LLM_DEVICE_MAP=auto
LLM_TORCH_DTYPE=float16
LLM_MAX_LENGTH=512
LLM_TEMPERATURE=0.7
LLM_TOP_P=0.9
LLM_DO_SAMPLE=true

# ChromaDB Configuration
CHROMA_PERSIST_DIRECTORY=./chroma_db
CHROMA_COLLECTION_NAME=codelearn_documents
CHROMA_EMBEDDING_MODEL=all-MiniLM-L6-v2
"""
    
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        print(f"\n✅ .env file created successfully at: {env_file}")
        if not hf_token:
            print("\n⚠️  Warning: You need to add your HuggingFace token to the .env file!")
            print("   Edit the file and replace 'your_token_here' with your actual token.")
    except Exception as e:
        print(f"\n❌ Error creating .env file: {e}")
        return
    
    print("\n" + "="*60)
    print("Setup complete! You can now start the server.")
    print("="*60 + "\n")

if __name__ == "__main__":
    create_env_file()
