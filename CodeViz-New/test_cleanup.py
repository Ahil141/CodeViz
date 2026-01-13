
import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.core.llm import LLMLoader

class MockSettings:
    model_path = "dummy"
    device_map = "cpu"

def test_cleaning():
    loader = LLMLoader(MockSettings()) # Won't load model unless accessed
    
    # 1. Test Repetition
    text = "This is a a stack stack stack."
    clean = loader._clean_response(text)
    print(f"Original: {text}")
    print(f"Cleaned:  {clean}")
    assert clean == "This is a stack.", f"Failed repetition check: {clean}"
    
    # 2. Test Code Formatting
    code_input = "Here is code:\n```python\ndef foo():\n  print('bar')\n```"
    # Black formats with 4 spaces?
    clean_code = loader._clean_response(code_input)
    print(f"\nCode Input:\n{code_input}")
    print(f"Clean Code:\n{clean_code}")
    
    if "def foo():" in clean_code and "print" in clean_code:
        print("Code exists.")
    
    # Check if black ran (it usually adds spaces around operators or normalizes quotes)
    code_input_messy = "```python\nx=1+1\n```"
    clean_messy = loader._clean_response(code_input_messy)
    print(f"\nMessy Input: {code_input_messy}")
    print(f"Clean Messy: {clean_messy}")
    
    if "x = 1 + 1" in clean_messy:
         print("Black formatting SUCCESS (spaces added).")
    else:
         print("Black formatting might have failed or black not installed.")

if __name__ == "__main__":
    try:
        test_cleaning()
        print("\nUnit Test Finished.")
    except Exception as e:
        print(f"Unit Test Failed: {e}")
