import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM
import asyncio
from llm_queue import summary_queue, queue_worker

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
    app.state.model = None
    app.state.tokenizer = None

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
