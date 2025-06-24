import redis
from rq import Queue
from llm.tasks import save_summary_task

redis_conn = redis.Redis(host='redis', port=6379)
queue = Queue('summaries', connection=redis_conn)

def save_summary_to_db(request_data, summary: str):
    queue.enqueue(
        save_summary_task,
        request_data["name"],
        summary,
        request_data["timestamp"]
    )
