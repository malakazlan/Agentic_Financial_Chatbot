from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Load once (global)
tokenizer = AutoTokenizer.from_pretrained("tiiuae/falcon-rw-1b")
model = AutoModelForCausalLM.from_pretrained("tiiuae/falcon-rw-1b")

def get_llm_response(prompt, context=""):
    full_prompt = f"{context}\nUser: {prompt}\nBot:"

    inputs = tokenizer(full_prompt, return_tensors="pt", truncation=True)
    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=200, do_sample=True)

    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Optional: clean up generated response
    if "Bot:" in result:
        result = result.split("Bot:")[-1].strip()
    return result
