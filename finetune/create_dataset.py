import json
# import sys
# import os
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# from ingestion.loaders import load_document
# from ingestion.chunker import chunk_text

# # file_path = "uploads/3d899bcb-8302-4fee-af45-82a0fb1450e9_python_program.pdf"
# file_path = "sample_lecture.txt"

# text = load_document(file_path)

# chunks = chunk_text(text, chunk_size=500, chunk_overlap=50)

# print(f"Loaded {len(chunks)} chunks from document")

# for i, chunk in enumerate(chunks):
#     print(f"\n--- Chunk {i} ---")
#     print(chunk[:200])

qa_pairs = [
    {
        "question":"What is Python known for?",
        "answer":"Python is a high-level, interpreted programming language known for its readability and simplicity."
    },

    {
        "question": "How do you create a variable in Python?",
        "answer": "A variable is created the moment you first assign a value to it. Python has no command for declaring a variable separately."
    },

    {
        "question": "What is a function in Python?",
        "answer": "A function in Python is a block of reusable code that performs a specific task, defined using the def keyword."
    },
    {
        "question": "What are the two main types of loops in Python?",
        "answer": "The two main types of loops in Python are the for loop and the while loop."
    },
    {
        "question": "What is a list in Python?",
        "answer": "A list in Python is an ordered, mutable collection of items, defined using square brackets."
    },
    {
        "question": "What is a dictionary in Python?",
        "answer": "A dictionary in Python is a collection of key-value pairs, defined using curly braces."
    },
]

with open("finetune/dataset.jsonl", "w")as f:
    for pair in qa_pairs:
        f.write(json.dumps(pair) + "\n")

print(f"Saved {len(qa_pairs)} question-answer pairs to finetune/dataset.jsonl")        