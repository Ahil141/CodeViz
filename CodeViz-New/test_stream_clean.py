
import re

def clean_stream_mock(text_chunks):
    buffer = ""
    yielded_text = ""
    
    print("Chunks input:", text_chunks)
    
    for new_text in text_chunks:
        print(f"Processing chunk: '{new_text}'")
        buffer += new_text
        
        if ' ' in buffer or '\n' in buffer:
            # Clean buffer
            cleaned_buffer = re.sub(r'\b(\w+)(\s+\1)+\b', r'\1', buffer, flags=re.IGNORECASE)
            print(f"  Cleaned buffer: '{cleaned_buffer}'")
            
            last_space = max(cleaned_buffer.rfind(' '), cleaned_buffer.rfind('\n'))
            
            if last_space != -1:
                to_yield = cleaned_buffer[:last_space+1]
                remaining = cleaned_buffer[last_space+1:]
                
                if to_yield:
                    print(f"  Yielding: '{to_yield}'")
                    yield to_yield
                    yielded_text += to_yield
                
                buffer = remaining
            else:
                 if len(cleaned_buffer) > 50:
                    yield cleaned_buffer
                    yielded_text += cleaned_buffer
                    buffer = ""
                 else:
                    buffer = cleaned_buffer
    
    if buffer:
        cleaned_buffer = re.sub(r'\b(\w+)(\s+\1)+\b', r'\1', buffer, flags=re.IGNORECASE)
        print(f"  Final Yield: '{cleaned_buffer}'")
        yield cleaned_buffer
        yielded_text += cleaned_buffer
        
    return yielded_text

def test_stream_cleaner():
    # Test Case 1: "A A Stack Stack "
    inputs = ["A ", "A ", "Sta", "ck ", "Sta", "ck ", "in"]
    print("\n--- Test 1 ---")
    result_1 = ""
    for chunk in clean_stream_mock(inputs):
        result_1 += chunk
    print(f"Result: '{result_1}'")
    assert result_1 == "A Stack in", f"Failed Test 1: {result_1}"
    
    # Test Case 2: Normal Sentence
    inputs_2 = ["Hello ", "world.", " How ", "are ", "you?"]
    print("\n--- Test 2 ---")
    result_2 = ""
    for chunk in clean_stream_mock(inputs_2):
        result_2 += chunk
    print(f"Result 2: '{result_2}'")
    assert result_2 == "Hello world. How are you?", f"Failed Test 2: {result_2}"

    # Test Case 3: Partial Repeats "Stutter Strutter" (Should NOT clean)
    inputs_3 = ["Stutter ", "Strutter"]
    print("\n--- Test 3 ---")
    result_3 = ""
    for chunk in clean_stream_mock(inputs_3):
        result_3 += chunk
    print(f"Result 3: '{result_3}'")
    assert result_3 == "Stutter Strutter", f"Failed Test 3: {result_3}"

if __name__ == "__main__":
    try:
        test_stream_cleaner()
        print("\nAll Stream Tests Passed!")
    except AssertionError as e:
        print(e)
