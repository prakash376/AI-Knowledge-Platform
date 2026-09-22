from transformers import AutoTokenizer, AutoModel
import torch

tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-small")

model = AutoModel.from_pretrained("google/flan-t5-small")

text = "Python is a great programming language."

inputs = tokenizer(text, return_tensors="pt")

with torch.no_grad():
    outputs = model.encoder(**inputs)

hidden_states = outputs.last_hidden_state  

print("Shape of hidden states:",hidden_states.shape)

print("First token's vector (first 10 numbers):", hidden_states[0][0][:10])