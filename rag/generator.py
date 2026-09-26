import os
from dotenv import load_dotenv

load_dotenv()  # reads .env file if it exists

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

_tokenizer = None
_model = None


def get_generator_model():
    """Loads the local flan-t5-base model (used when no API key is set)."""
    global _tokenizer, _model
    if _model is None:
        from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
        _tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
        _model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")
    return _tokenizer, _model


def generator_answer(question: str, context: str) -> str:
    if OPENAI_API_KEY:
        return _generate_with_openai(question, context)
    return _generate_with_local_model(question, context)


def _generate_with_local_model(question: str, context: str) -> str:
    tokenizer, model = get_generator_model()

    prompt = f"Answer the question based on the context. Include an example if one is given.\n\nContext: {context}\n\nQuestion: {question}"
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)

    output_ids = model.generate(
        **inputs,
        max_new_tokens=150,
        repetition_penalty=1.5,
        no_repeat_ngram_size=3,
    )
    return tokenizer.decode(output_ids[0], skip_special_tokens=True)


def _generate_with_openai(question: str, context: str) -> str:
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY)

    prompt = f"Answer the question based on the context. Include an example if one is given.\n\nContext: {context}\n\nQuestion: {question}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
    )
    return response.choices[0].message.content