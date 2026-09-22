from rag.generator import get_generator_model

def rewrite_query(current_question:str, history:list[str])->str:
    if not history:
        return current_question

    tokenizer , model = get_generator_model()

    history_text = "\n".join(history[-3:])

    prompt = (
        f"Given this conversation history:\n{history_text}\n\n"
        f"Rewrite this follow-up question as a standalone question:\n{current_question}"
        )     

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)

    output_ids = model.generate(**inputs, max_new_tokens=50)

    rewritten = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    return rewritten.strip()