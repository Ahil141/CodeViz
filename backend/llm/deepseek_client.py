import ollama

def generate(prompt: str) -> str:
    """
    Calls DeepSeek-Coder-1.3B running inside Ollama.
    Works with ollama version 0.6.1
    """
    try:
        resp = ollama.chat(
            model="deepseek-coder:1.3b",
            messages=[{"role": "user", "content": prompt}]
        )
        # Extract content from the response
        return resp.message.content if resp and resp.message else "LLM returned no output."
    except Exception as e:
        return f"Error communicating with DeepSeek model: {str(e)}"
