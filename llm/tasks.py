import requests

def save_summary_task(name: str, summary: str, timestamp: str):
    payload = {
        "content": summary,
        "timestamp": timestamp
    }

    response = requests.post(
        f"http://postgres_api:5011/summaries/{name}",
        json=payload
    )

    if response.status_code != 201:
        raise Exception(f"Nie udało się zapisać streszczenia: {response.text}")
