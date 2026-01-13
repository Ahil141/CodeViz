
import re

def mock_stream_logic():
    # Simulation of stream_generate logic
    chunks = ["The", " ", "The", " ", "quick", " ", "quick", " ", "brown", " ", "brown"]
    # or maybe tokens: ["The", " The", " quick", " quick"] depending on tokenizer
    # Let's try mimicking the user report: "The The quick quick"
    
    context = ""
    buffer = ""
    
    print(f"Input chunks: {chunks}")
    print("Output:", end="")
    
    for new_text in chunks:
        # Logic from llm.py
        full_text = context + buffer + new_text
        
        # Regex: Remove immediate word repetitions
        cleaned_full = re.sub(r'\b(\w+)(\s+\1)+\b', r'\1', full_text, flags=re.IGNORECASE)
        
        if cleaned_full.startswith(context):
            buffer = cleaned_full[len(context):]
        elif context.startswith(cleaned_full):
            # The cleaning collapsed the text into the existing context
            # We ignore the new tokens as they are repetitions
            buffer = ""
        else:
            # Fallback
            buffer = (buffer + new_text)
        
        last_space = max(buffer.rfind(' '), buffer.rfind('\n'))
        
        if last_space != -1:
            to_yield = buffer[:last_space+1]
            remaining = buffer[last_space+1:]
            
            if to_yield:
                print(f"'{to_yield}'", end="|")
                context += to_yield
                if len(context) > 200:
                    context = context[-200:]
            
            buffer = remaining

    if buffer:
        full_text = context + buffer
        cleaned_full = re.sub(r'\b(\w+)(\s+\1)+\b', r'\1', full_text, flags=re.IGNORECASE)
        if cleaned_full.startswith(context):
            final_yield = cleaned_full[len(context):]
            print(f"'{final_yield}'", end="|")
        else:
            print(f"'{buffer}'", end="|")

if __name__ == "__main__":
    mock_stream_logic()
