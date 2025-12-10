def build_prompt(user_query, retrieved_code):
    return f"""
You are a helpful Data Structures tutor.

User query:
{user_query}

Relevant code retrieved from database:
{retrieved_code}

Your tasks:
1. Explain the data structure simply.
2. Explain how the code works step-by-step.
3. Give a clean and formatted version of the code.
4. Do NOT add wrong information.
"""
