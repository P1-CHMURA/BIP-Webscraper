import asyncio
from database import save_summary_to_db
from summarizer import summarize_with_model

summary_queue = asyncio.Queue()

async def queue_worker(app):
    while True:
        request_data = await summary_queue.get()
        try:
            summary = await summarize_with_model(app, request_data["content"])
            await save_summary_to_db(request_data, summary)
        except Exception as e:
            print(f"[KOLEJKA] Błąd przetwarzania: {e}")
        finally:
            summary_queue.task_done()
