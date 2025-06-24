import httpx

async def save_summary_to_db(request_data, summary: str):
    async with httpx.AsyncClient() as client:
        payload = {
            "content": summary,
            "timestamp": request_data["timestamp"]
        }
        response = await client.post(
            f"http://postgres_api:5011/summaries/{request_data['name']}",
            json=payload
        )

        if response.status_code != 201:
            raise Exception(f"Nie udało się zapisać streszczenia: {response.text}")
