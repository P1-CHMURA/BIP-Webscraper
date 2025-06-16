import torch
import re
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from transformers import AutoTokenizer, AutoModelForCausalLM
from contextlib import asynccontextmanager

MODEL_NAME = "Qwen/Qwen3-1.7B-FP8"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def lifespan(app: FastAPI):
    try:
        model_path = "/app/model"
        tokenizer_path = "/app/tokenizer"
        
        app.state.tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
        app.state.model = AutoModelForCausalLM.from_pretrained(model_path, device_map="auto")
        
        logger.info("Model i tokenizer zostały pomyślnie załadowane.")
    except Exception as e:
        logger.error(f"Błąd podczas ładowania modelu: {e}")
        app.state.model = None
        app.state.tokenizer = None

    yield
    app.state.model = None
    app.state.tokenizer = None


class LLMRequest(BaseModel):
    source: str = Field(..., description="Źródło dokumentu")
    name: str = Field(..., description="Nazwa dokumentu")
    typ: str = Field(..., description="Typ dokumentu")
    content: str = Field(..., description="Zawartość tekstowa dokumentu")
    timestamp: str = Field(..., description="Znacznik czasu")
    status: str = Field(..., description="Status dokumentu")

app = FastAPI(
    title="Mikroserwis Podsumowujący Dane",
    description="API, które używa lokalnego modelu Qwen 3 do podsumowania tekstu.",
    version="1.0.0",
    lifespan=lifespan,
)

@app.post("/summarize", summary="Podsumuj tekst")
def summarize_data(request: LLMRequest):
    """
    Ten endpoint przyjmuje wcześniej wyznaczone różnice między dokumentami, a następnie je podsumowuje.
    """
    if not app.state.model or not app.state.tokenizer:
        raise HTTPException(
            status_code=503,
            detail="Model AI nie jest dostępny. Sprawdź logi serwera."
        )

    logger.info(f"Input text to model: {request.content}")
    prompt_text = f"""
    Summarize below text.

    ### Text to summarize:
    {request.content}
    """
    
    chat = [
        {"role": "user", "content": prompt_text},
    ]
    
    input_ids = app.state.model.apply_chat_template(chat, tokenize=True, add_generation_prompt=True, return_tensors="pt")
    input_ids = input_ids.to(app.state.model.device)

    try:
        outputs = app.state.model.generate(
            input_ids,
            max_new_tokens=1028,
            do_sample=True,
            temperature=0.6
        )
        
        raw_analysis_result = app.state.model.decode(outputs[0][input_ids.shape[-1]:], skip_special_tokens=True).strip()

        logger.info(f"Raw output from model: {raw_analysis_result}")
        
        cleaned_analysis_result = re.sub(r'<think>.*?</think>', '', raw_analysis_result, flags=re.DOTALL).strip()
        
        if not cleaned_analysis_result:
            cleaned_analysis_result = raw_analysis_result

        return {"analysis": cleaned_analysis_result}
        

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Wystąpił błąd podczas generowania odpowiedzi przez model: {e}"
        )

@app.get("/")
def read_root():
    return {"message": "Witaj w API do porównywania tekstów!"}