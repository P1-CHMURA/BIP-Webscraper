import requests
import time

def save_summary_task(name: str, summary: str, timestamp: str):
    payload = {
        "content": summary,
        "timestamp": timestamp
    }

    max_retries = 3
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            response = requests.post(
                f"http://postgres_api:5011/summaries/{name}",
                json=payload,
                timeout=10
            )
            
            if response.status_code == 201:
                print(f"Streszczenie zapisane pomyślnie dla: {name}")
                return
            else:
                print(f"Błąd API (próba {attempt + 1}): {response.status_code} - {response.text}")
                
        except requests.exceptions.ConnectionError as e:
            print(f"Błąd połączenia (próba {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                print(f"Ponowienie za {retry_delay} sekund...")
                time.sleep(retry_delay)
                retry_delay *= 2
            else:
                raise Exception(f"Nie udało się połączyć z postgres_api po {max_retries} próbach")
                
        except requests.exceptions.Timeout as e:
            print(f"Timeout (próba {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                raise Exception(f"Timeout po {max_retries} próbach")
                
        except Exception as e:
            print(f"Nieoczekiwany błąd: {e}")
            raise
    
    raise Exception(f"Nie udało się zapisać streszczenia po {max_retries} próbach")