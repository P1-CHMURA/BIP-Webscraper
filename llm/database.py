import redis
from rq import Queue
from tasks import save_summary_task
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

redis_conn = redis.Redis(host='llm_redis', port=6379)
queue = Queue('summaries', connection=redis_conn)

def save_summary_to_db(request_data, summary: str):
    logger.info(f"Nazwa dokumentu {request_data['name']}")
    queue.enqueue(
        save_summary_task,
        request_data["name"],
        summary,
        request_data["timestamp"]
    )