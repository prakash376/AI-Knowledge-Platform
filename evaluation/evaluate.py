import sys 
import os 
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from peft import PeftModel

with open ("finetune/dataset.jsonl")as f:
    test_cases = [json.loads(line) for line in f]

base_model_name = "google/flan-t5-small"
adapter_path = "finetune/my_adapter"

base_tokneizer = AutoTokenizer.from_pretrained(base_model_name)
base_model = AutoModelForSeq2SeqLM.from_pretrained(base_model_name)

ft_tokenizer = AutoTokenizer.from_pretrained(adapter_path)
ft_base = AutoModelForSeq2SeqLM.from_pretrained(base_model_name)
ft_model = PeftModel.from_pretrained(ft_base, adapter_path)

def generate_answer(tokenizer,model,question):
    inputs = tokenizer(question , return_tensors="pt")
    output_ids = model.generate(**inputs,max_new_tokens=64)
    return tokenizer.decode(output_ids[0], skip_special_tokens=True)

def keyword_overlap_score(expected: str , actual: str)-> float:
    expected_words = set(expected.lower().split())
    actual_words = set(actual.lower().split())
    if not expected_words:
        return 0.0
    overlap = expected_words & actual_words
    return len(overlap) / len(expected_words)


base_scores = []
ft_scores = []

for case in test_cases:
    question = case["question"]
    expected = case["answer"]

    base_answer = generate_answer(base_tokneizer, base_model, question)
    ft_answer = generate_answer(ft_tokenizer, ft_model, question)

    base_score = keyword_overlap_score(expected, base_answer)
    ft_score = keyword_overlap_score(expected, ft_answer)

    base_scores.append(base_score)
    ft_scores.append(ft_score)

    print(f"{question[:43]:<45} | {base_score:<10.2f} | {ft_score:<16.2f}")

print("-" * 80)
print(f"Average base model score:       {sum(base_scores)/len(base_scores):.2f}")
print(f"Average fine-tuned model score: {sum(ft_scores)/len(ft_scores):.2f}")