
import re

def clean_stream_context_mock(text_chunks):
    buffer = ""
    context = ""
    yielded_text = ""
    
    print(f"Chunks: {text_chunks}")
    
    for new_text in text_chunks:
        # We append to buffer, but we check regex against (context + buffer)
        # However, we can't change context.
        # So we clean (context + buffer), then subtract context to get "valid buffer".
        
        current_buffer = buffer + new_text
        full_text = context + current_buffer
        
        # Clean the full text
        # Regex to remove IMMEDIATE repetition
        cleaned_full = re.sub(r'\b(\w+)(\s+\1)+\b', r'\1', full_text, flags=re.IGNORECASE)
        
        # Now we need to determine what part of current_buffer remains
        # Ideally cleaned_full startswith context.
        # But if the repetition crossed the boundary, cleaned_full might be SHORTER than context?
        # Ex: Context="Stack ". Buffer="Stack". Full="Stack Stack". Cleaned="Stack ".
        # Context="Stack ". Cleaned="Stack ".
        # So Cleaned is same as Context.
        # New valid buffer content is Cleaned - Context.
        
        if len(cleaned_full) < len(context):
            # This implies the context itself was repetitive? 
            # Or the match consumed the context?
            # matches "Stack Stack" -> "Stack". 
            # If Context="Stack ", Buffer="Stack". Match="Stack ".
            # len(cleaned)=6. len(context)=6.
            # So new part is empty.
            pass
        
        # We assume context is immutable (already yielded).
        # But if the regex changes the *end* of context?
        # Actually, regex `\b(\w+)(\s+\1)+\b` only collapses the *second* occurrence?
        # "Stack Stack" -> "Stack".
        # Yes, it keeps the FIRST one.
        # So the Context (the past) is preserved. The repetition (the future) is removed.
        # So `cleaned_full` should always start with `context` (roughly).
        
        if not cleaned_full.startswith(context):
            # This happens if we cleaned something INSIDE context?
            # Or if case changed?
            print(f"CRITICAL: Context mismatch. Cleaned '{cleaned_full}' vs Context '{context}'")
            # Fallback: just use buffer
            buffer = current_buffer
        else:
            # The effective buffer is the part after context
            buffer = cleaned_full[len(context):]
            
        print(f"  Chunk '{new_text}' -> Full '{full_text}' -> Cleaned '{cleaned_full}' -> NewBuffer '{buffer}'")
            
        # Now decide what to yield from BUFFER
        # We yield up to the last safety boundary (space/newline)
        last_space = max(buffer.rfind(' '), buffer.rfind('\n'))
        
        if last_space != -1:
            to_yield = buffer[:last_space+1]
            remaining = buffer[last_space+1:]
            
            if to_yield:
                yield to_yield
                context += to_yield
                yielded_text += to_yield
                # Keep context small (optional, but good for regex perf)
                if len(context) > 100:
                    context = context[-100:]
            
            buffer = remaining

    # Yield remaining
    if buffer:
        yield buffer
        yielded_text += buffer

    return yielded_text

def test_stream_context():
    # Test 1: "A A Stack Stack "
    inputs = ["A ", "A ", "Sta", "ck ", "Sta", "ck ", "in"]
    print("\n--- Test 1 ---")
    res = ""
    for c in clean_stream_context_mock(inputs):
        res += c
    print(f"Result: '{res}'")
    assert res == "A Stack in", f"Failed Test 1: '{res}'"

    # Test 2: Context cut
    inputs_2 = ["Hello ", "world ", "world ", "again"]
    print("\n--- Test 2 ---")
    res_2 = ""
    for c in clean_stream_context_mock(inputs_2):
        res_2 += c
    print(f"Result: '{res_2}'")
    assert res_2.strip() == "Hello world again", f"Failed Test 2: '{res_2}'"

if __name__ == "__main__":
    try:
        test_stream_context()
        print("\nPASSED all context tests.")
    except AssertionError as e:
        print(e)
