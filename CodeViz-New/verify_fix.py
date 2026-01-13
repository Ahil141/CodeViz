import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.getcwd(), 'backend'))

from app.core.visualizers import get_default_visualizer

def test_visualizer_selection():
    test_cases = [
        ("Doubly Linked List", "Doubly Linked List"),
        ("Circular Doubly Linked List", "Circular Doubly Linked List"),
        ("Singly Linked List", "Singly Linked List"),
        ("Circular Linked List", "Circular Linked List"),
        ("Linked List", "Singly Linked List"), # Generic fallbacks
        ("Unknown Structure", None)
    ]

    print("Running Visualizer Selection Tests...")
    all_passed = True
    
    for input_name, expected_name in test_cases:
        result = get_default_visualizer(input_name)
        if expected_name is None:
            if result is None:
                 print(f"[PASS] Input: '{input_name}' -> Correctly returned None")
            else:
                 print(f"[FAIL] Input: '{input_name}' -> Expected None, got '{result['name']}'")
                 all_passed = False
        else:
            if result and result['name'] == expected_name:
                print(f"[PASS] Input: '{input_name}' -> Correctly returned '{result['name']}'")
            else:
                got = result['name'] if result else "None"
                print(f"[FAIL] Input: '{input_name}' -> Expected '{expected_name}', got '{got}'")
                all_passed = False

    if all_passed:
        print("\nAll tests passed! The fix is verified.")
    else:
        print("\nSome tests failed.")

if __name__ == "__main__":
    test_visualizer_selection()
