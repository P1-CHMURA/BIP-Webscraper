# Komenda do odpalenia
# uvicorn main:app --reload
#
# http://127.0.0.1:8000/docs#/default/
#
import torch
import re
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from transformers import AutoTokenizer, AutoModelForCausalLM

# --- Krok 1: Konfiguracja i ładowanie modelu ---

MODEL_NAME = "Qwen/Qwen3-1.7B"  

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Używane urządzenie: {device}")

# Ustawienie typu danych
torch_dtype = torch.bfloat16 if torch.cuda.is_available() and torch.cuda.is_bf16_supported() else torch.float32

try:
    # Załaduj tokenizer
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype=torch_dtype,
    )
    model.to(device)
    
    print("Model i tokenizer zostały pomyślnie załadowane.")
except Exception as e:
    print(f"Błąd podczas ładowania modelu: {e}")
    model = None
    tokenizer = None


# --- Definicja modelu danych wejściowych ---
class ComparisonRequest(BaseModel):
    old_data: str = Field(..., min_length=1, description="Pierwsza, starsza wersja danych do porównania.")
    new_data: str = Field(..., min_length=1, description="Druga, nowsza wersja danych do porównania.")

# --- Inicjalizacja aplikacji FastAPI ---
app = FastAPI(
    title="Mikroserwis Porównujący Dane",
    description="API, które używa lokalnego modelu Qwen 3 do porównywania dwóch tekstów i znajdowania różnic.",
    version="1.0.0"
)

# --- Krok 2: Modyfikacja endpointu API ---
@app.post("/compare", summary="Porównaj dwa teksty")
def compare_data(request: ComparisonRequest):
    """
    Ten endpoint przyjmuje dwie wersje danych, wysyła je do lokalnego modelu
    załadowanego w pamięci i zwraca podsumowanie zmian.
    """
    if not model or not tokenizer:
        raise HTTPException(
            status_code=503,
            detail="Model AI nie jest dostępny. Sprawdź logi serwera."
        )


    prompt_text = f"""
    Compare "OLD VERSION" with "NEW VERSION" and print changes between the texts.
    If there are no changes, print "Brak zmian".

    ### OLD VERSION:
    {request.old_data}

    ### NEW VERSION:
    {request.new_data}
    """
    
    chat = [
        {"role": "user", "content": prompt_text},
    ]
    
    # Zastosuj szablon czatu i przekonwertuj na tensory
    input_ids = tokenizer.apply_chat_template(chat, tokenize=True, add_generation_prompt=True, return_tensors="pt")
    input_ids = input_ids.to(device) 

    # --- Generowanie odpowiedzi przez model ---
    try:
        # Generowanie tekstu. `max_new_tokens` ogranicza długość odpowiedzi.
        outputs = model.generate(
            input_ids,
            max_new_tokens=1028,
            do_sample=True,
            temperature=0.6
        )
        
        # Dekodowanie surowej odpowiedzi z modelu
        raw_analysis_result = tokenizer.decode(outputs[0][input_ids.shape[-1]:], skip_special_tokens=True).strip()

        print("--- Surowa odpowiedź modelu (z blokiem <think>) ---")
        print(raw_analysis_result)
        print("-------------------------------------------------")
        
        cleaned_analysis_result = re.sub(r'<think>.*?</think>', '', raw_analysis_result, flags=re.DOTALL).strip()
        
        if not cleaned_analysis_result:
            cleaned_analysis_result = raw_analysis_result

        return {"analysis": cleaned_analysis_result}
        

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Wystąpił błąd podczas generowania odpowiedzi przez model: {e}"
        )

# --- Endpoint powitalny (bez zmian) ---
@app.get("/")
def read_root():
    return {"message": "Witaj w API do porównywania tekstów!"}