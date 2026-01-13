
import os
import threading
import time
from transformers import AutoTokenizer, AutoModelForCausalLM, TextIteratorStreamer
import torch

# Force CPU threads to 1 to mimic fixing potential deadlocks
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

MODEL_NAME = "Qwen/Qwen2.5-Coder-1.5B-Instruct"

def test_generation():
    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
        
    print("Loading model...")
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME, 
        device_map="cpu", 
        torch_dtype=torch.float32, 
        trust_remote_code=True,
        attn_implementation="eager"
    )
    print("Model loaded.")

    prompt = "Write a python function to add two numbers."
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
    
    streamer = TextIteratorStreamer(tokenizer, skip_prompt=True)
    
    generation_kwargs = dict(
        inputs,
        streamer=streamer,
        max_new_tokens=64,
        do_sample=False,
        pad_token_id=tokenizer.eos_token_id,
        eos_token_id=tokenizer.eos_token_id,
        use_cache=True, # Testing if this is the issue
        temperature=None,
        top_p=None
    )
    
    print("Starting generation thread...")
    thread = threading.Thread(target=model.generate, kwargs=generation_kwargs)
    thread.start()
    
    print("Iterating streamer...")
    start_time = time.time()
    generated_text = ""
    try:
        for new_text in streamer:
            print(f"Token: {new_text!r}")
            generated_text += new_text
            if time.time() - start_time > 30:
                print("TIMEOUT REACHED!")
                break
    except Exception as e:
        print(f"Error during streaming: {e}")

    print("Generation finished.")
    print("Full text:", generated_text)

if __name__ == "__main__":
    test_generation()
