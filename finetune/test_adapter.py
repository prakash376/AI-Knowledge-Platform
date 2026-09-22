import sys
import os 
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from peft import PeftModel

base_model_name =  "google/flan-t5-small"
adapter_path = "finetune/my_adapter"

tokenizer = AutoTokenizer.from_pretrained(adapter_path)
base_model = AutoModelForSeq2SeqLM.from_pretrained(base_model_name)
model = PeftModel.from_pretrained(base_model,adapter_path)

question = "What is a function in Python?"
inputs = tokenizer(question , return_tensors="pt")
output_ids = model.generate(**inputs, max_new_tokens=64)
answer = tokenizer.decode(output_ids[0], skip_special_tokens=True)

print(f"Question: {question}")
print(f"Fine-tuned model's answer: {answer}")