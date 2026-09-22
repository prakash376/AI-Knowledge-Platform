from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

_tokenizer = None
_model = None


def get_generator_model():
    global _tokenizer, _model
    if _model is None:
        _tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-small")
        _model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small")
    return _tokenizer , _model


def generator_answer(question: str, context: str) -> str:
    tokenizer , model = get_generator_model()
    prompt =f"Answer the question based on the context.\n\nContext: {context}\n\nQuestion: {question}"
    result = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
    output_ids = model.generate(**result, max_new_tokens=100)
    answer = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    return answer