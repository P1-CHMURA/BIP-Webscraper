from transformers import AutoTokenizer, AutoModelForCausalLM
import os

def preload_model(model_name: str, model_dir: str):
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto")

        os.makedirs(f"{model_dir}/tokenizer", exist_ok=True)
        os.makedirs(f"{model_dir}/model", exist_ok=True)

        tokenizer.save_pretrained(f"{model_dir}/tokenizer")
        model.save_pretrained(f"{model_dir}/model")

        print("Model i tokenizer zostały pomyślnie załadowane i zapisane.")
    except Exception as e:
        print(f"Błąd podczas ładowania i zapisywania modelu: {e}")
        raise

if __name__ == "__main__":
    model_name = 'Qwen/Qwen3-1.7B'
    model_dir = '/app'
    preload_model(model_name, model_dir)