import torch
import re
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from transformers import AutoTokenizer, AutoModelForCausalLM
from llm.queue import summary_queue, queue_worker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMRequest(BaseModel):
    source: str
    name: str
    typ: str
    content: str
    timestamp: str
    status: str

async def lifespan(app: FastAPI):
    try:
        model_path = "/app/model"
        tokenizer_path = "/app/tokenizer"
        
        app.state.tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
        app.state.model = AutoModelForCausalLM.from_pretrained(model_path, device_map="auto")
        
        logger.info("Model i tokenizer załadowane.")
        
        app.state.queue_task = asyncio.create_task(queue_worker(app))
    except Exception as e:
        logger.error(f"Błąd ładowania modelu: {e}")
        app.state.model = None
        app.state.tokenizer = None

    yield
    app.state.queue_task.cancel()

app = FastAPI(title="Mikroserwis LLM", lifespan=lifespan)

@app.post("/summarize", summary="Zleć podsumowanie do kolejki")
async def summarize_data(request: LLMRequest):
    if not app.state.model or not app.state.tokenizer:
        raise HTTPException(status_code=503, detail="Model niedostępny.")
    if not request.content:
        raise HTTPException(status_code=400, detail="Brak treści.")

    await summary_queue.put(request.dict())
    return {"message": "Zlecenie dodane do kolejki."}

@app.get("/")
def read_root():
    return {"message": "LLM działa!"}

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
