import re

async def summarize_with_model(app, content: str) -> str:
    prompt_text = f"""
    Podsumuj poniższy tekst:

    {content}

    Podsumowanie:
    """
    messages = [{"role": "user", "content": prompt_text}]
    text = app.state.tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=False
    )
    inputs = app.state.tokenizer([text], return_tensors="pt").to(app.state.model.device)
    input_ids = inputs["input_ids"]

    outputs = app.state.model.generate(
        **inputs,
        max_new_tokens=1028,
        do_sample=True,
        temperature=0.6
    )

    generated_text = app.state.tokenizer.decode(
        outputs[0][input_ids.shape[-1]:], skip_special_tokens=True
    ).strip()

    cleaned = re.sub(r'<think>.*?</think>', '', generated_text, flags=re.DOTALL).strip()
    return cleaned if cleaned else generated_text