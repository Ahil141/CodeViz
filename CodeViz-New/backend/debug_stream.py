
import os
import sys
import threading
import time
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, TextIteratorStreamer

# Force CPU settings
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

MODEL_PATH = "microsoft/Phi-3.5-mini-instruct"

def load_model():
    print(f"Loading model from {MODEL_PATH}...")
    try:
        tokenizer = AutoTokenizer.from_pretrained(
            MODEL_PATH,
            trust_remote_code=True
        )
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
            
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_PATH,
            device_map="cpu",
            torch_dtype=torch.float32,
            trust_remote_code=True,
            attn_implementation="eager"
        )
        print("Model loaded successfully.")
        return tokenizer, model
    except Exception as e:
        print(f"Error loading model: {e}")
        sys.exit(1)

def stream_generate(tokenizer, model, prompt):
    print(f"\nGenerating response for: '{prompt}'")
    
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    
    streamer = TextIteratorStreamer(
        tokenizer, 
        skip_prompt=True, 
        skip_special_tokens=True
    )
    
    generation_kwargs = dict(
        inputs,
        streamer=streamer,
        max_new_tokens=128,
        do_sample=False,
        use_cache=True,
        pad_token_id=tokenizer.eos_token_id,
        eos_token_id=tokenizer.eos_token_id,
    )
    
    # Run generation in a separate thread
    thread = threading.Thread(target=model.generate, kwargs=generation_kwargs)
    thread.start()
    
    print("Stream output: ", end="", flush=True)
    generated_text = ""
    start_time = time.time()
    first_token = True
    
    for new_text in streamer:
        if first_token:
            print(f"\n[First token after {time.time() - start_time:.2f}s]")
            first_token = False
        print(new_text, end="", flush=True)
        generated_text += new_text
        
    print("\n\nGeneration complete.")
    return generated_text

if __name__ == "__main__":
    tokenizer, model = load_model()
    
    prompt = "<|user|>\nWrite a hello world program in Python<|end|>\n<|assistant|>"
    stream_generate(tokenizer, model, prompt)
