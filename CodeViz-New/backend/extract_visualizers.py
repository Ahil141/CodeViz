import os
import sys

# Add current directory to path to allow imports
sys.path.append(os.getcwd())

from app.core.visualizers import (
    STACK_VISUALIZER, QUEUE_VISUALIZER, LINKED_LIST_VISUALIZER,
    DOUBLY_LINKED_LIST_VISUALIZER, CIRCULAR_LINKED_LIST_VISUALIZER,
    CIRCULAR_DOUBLY_LINKED_LIST_VISUALIZER, SKIP_LIST_VISUALIZER,
    UNROLLED_LINKED_LIST_VISUALIZER, XOR_LINKED_LIST_VISUALIZER,
    DYNAMIC_ARRAY_VISUALIZER, SPARSE_ARRAY_VISUALIZER, JAGGED_ARRAY_VISUALIZER,
    CIRCULAR_ARRAY_VISUALIZER, ARRAY_VISUALIZER, BST_VISUALIZER,
    AVL_TREE_VISUALIZER, RED_BLACK_TREE_VISUALIZER, SPLAY_TREE_VISUALIZER,
    TREAP_VISUALIZER, SCAPEGOAT_TREE_VISUALIZER, B_PLUS_TREE_VISUALIZER,
    B_STAR_TREE_VISUALIZER, B_TREE_VISUALIZER, GENERAL_TREE_VISUALIZER,
    HEAP_VISUALIZER, FIBONACCI_HEAP_VISUALIZER, BINOMIAL_HEAP_VISUALIZER,
    PAIRING_HEAP_VISUALIZER, UNIFIED_GRAPH_VISUALIZER
)

OUTPUT_DIR = "rag/data/interactive"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Map Name -> (Visualizer Code, Description, Topic)
VISUALIZERS = {
    "Stack": (STACK_VISUALIZER, "Interactive Stack visualizer demonstrating LIFO operations", "Stack"),
    "Queue": (QUEUE_VISUALIZER, "Interactive Queue visualizer demonstrating FIFO operations", "Queue"),
    "Singly Linked List": (LINKED_LIST_VISUALIZER, "Interactive Singly Linked List visualizer", "Linked List"),
    "Doubly Linked List": (DOUBLY_LINKED_LIST_VISUALIZER, "Doubly Linked List Visualizer", "Linked List"),
    "Circular Linked List": (CIRCULAR_LINKED_LIST_VISUALIZER, "Circular Linked List Visualizer", "Linked List"),
    "Circular Doubly Linked List": (CIRCULAR_DOUBLY_LINKED_LIST_VISUALIZER, "CDLL Visualizer", "Linked List"),
    "Skip List": (SKIP_LIST_VISUALIZER, "Skip List Visualizer", "Linked List"),
    "Unrolled Linked List": (UNROLLED_LINKED_LIST_VISUALIZER, "Unrolled LL Visualizer", "Linked List"),
    "XOR Linked List": (XOR_LINKED_LIST_VISUALIZER, "XOR Linked List Visualizer", "Linked List"),
    "Dynamic Array": (DYNAMIC_ARRAY_VISUALIZER, "Dynamic Array (Vector)", "Array"),
    "Sparse Array": (SPARSE_ARRAY_VISUALIZER, "Sparse Array", "Array"),
    "Jagged Array": (JAGGED_ARRAY_VISUALIZER, "Jagged Array", "Array"),
    "Circular Array": (CIRCULAR_ARRAY_VISUALIZER, "Circular Array/Buffer", "Array"),
    "Array": (ARRAY_VISUALIZER, "Basic Array Visualizer", "Array"),
    "Binary Search Tree": (BST_VISUALIZER, "BST Visualizer", "Tree"),
    "AVL Tree": (AVL_TREE_VISUALIZER, "AVL Tree Visualizer", "Tree"),
    "Red-Black Tree": (RED_BLACK_TREE_VISUALIZER, "RB Tree Visualizer", "Tree"),
    "Splay Tree": (SPLAY_TREE_VISUALIZER, "Splay Tree Visualizer", "Tree"),
    "Treap": (TREAP_VISUALIZER, "Treap Visualizer", "Tree"),
    "Scapegoat Tree": (SCAPEGOAT_TREE_VISUALIZER, "Scapegoat Tree Visualizer", "Tree"),
    "B+ Tree": (B_PLUS_TREE_VISUALIZER, "B+ Tree Visualizer", "Tree"),
    "B* Tree": (B_STAR_TREE_VISUALIZER, "B* Tree Visualizer", "Tree"),
    "B-Tree": (B_TREE_VISUALIZER, "B-Tree Visualizer", "Tree"),
    "General Tree": (GENERAL_TREE_VISUALIZER, "N-ary Tree Visualizer", "Tree"),
    "Min Heap": (HEAP_VISUALIZER, "Min Heap Visualizer", "Heap"),
    "Max Heap": (HEAP_VISUALIZER, "Max Heap Visualizer", "Heap"),
    "Fibonacci Heap": (FIBONACCI_HEAP_VISUALIZER, "Fibonacci Heap", "Heap"),
    "Binomial Heap": (BINOMIAL_HEAP_VISUALIZER, "Binomial Heap", "Heap"),
    "Pairing Heap": (PAIRING_HEAP_VISUALIZER, "Pairing Heap", "Heap"),
    "Graph": (UNIFIED_GRAPH_VISUALIZER, "Unified Graph Visualizer (Directed/Weighted/Undirected)", "Graph"),
}

print(f"Extracting {len(VISUALIZERS)} visualizers to {OUTPUT_DIR}...")

for name, (code, description, topic) in VISUALIZERS.items():
    safe_name = name.replace(" ", "_").replace("*", "Star").replace("+", "Plus")
    filename = os.path.join(OUTPUT_DIR, f"{safe_name}.txt")
    
    content = f"""### DOCUMENT_TYPE: INTERACTIVE
### TOPIC: {topic}
### NAME: {name}
### DESCRIPTION: {description}

{code}"""
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"Authored: {filename}")

print("Extraction complete.")
