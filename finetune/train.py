import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, TrainingArguments, Trainer
from peft import LoraConfig, get_peft_model, TaskType

dataset = load_dataset("json", data_files="finetune/dataset.jsonl")["train"]
print(f"Loaded {len(dataset)} training examples.")

model_name = "google/flan-t5-small"

tokenizer = AutoTokenizer.from_pretrained(model_name)
base_model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

lora_config = LoraConfig(
    task_type=TaskType.SEQ_2_SEQ_LM,
    r=8,
    lora_alpha=16,
    lora_dropout=0.1,
    target_modules=["q", "v"],
)

model = get_peft_model(base_model, lora_config)
model.print_trainable_parameters()


def preprocess(example):
    inputs = tokenizer(example["question"], truncation=True, padding="max_length", max_length=64)
    labels = tokenizer(example["answer"], truncation=True, padding="max_length", max_length=64)
    inputs["labels"] = labels["input_ids"]
    return inputs


tokenized_dataset = dataset.map(preprocess)

training_args = TrainingArguments(
    output_dir="finetune/output",
    num_train_epochs=30,
    per_device_train_batch_size=2,
    learning_rate=3e-4,
    logging_steps=1,
    save_strategy="no",
    report_to=[],
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
)

trainer.train()

model.save_pretrained("finetune/my_adapter")
tokenizer.save_pretrained("finetune/my_adapter")
print("Fine-tuning complete! Adapter saved to finetune/my_adapter")