from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-small")

text =  "Python is a great programming language."

tokens = tokenizer.tokenize(text)
print("Tokens:", tokens)

input_ids = tokenizer.encode(text)
print("Input IDs:", input_ids)

decoded = tokenizer.decode(input_ids)
print("Decoded Back:", decoded)