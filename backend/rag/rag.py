# rag/rag.py

from .vectordb import search
from .prompt_builder import build_prompt
from llm.deepseek_client import generate  # Your DeepSeek LLM client

def answer(query: str) -> str:
    """
    Main RAG function: 
    1. Retrieve code from Chroma DB via vectordb.py
    2. Build a prompt for DeepSeek
    3. Generate the final answer
    """
    # Step 1: Retrieve code snippet from vector DB
    retrieved_code = search(query)

    # Step 2: Build prompt for DeepSeek
    prompt = build_prompt(query, retrieved_code)

    # Step 3: Get LLM output
    llm_output = generate(prompt)
    return llm_output
