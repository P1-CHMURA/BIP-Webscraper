import redis
from rq import Worker, Queue

listen = ['summaries']

redis_conn = redis.Redis(host='llm_redis', port=6379)

if __name__ == '__main__':
    queue = Queue(name='summaries', connection=redis_conn)
    worker = Worker([queue], connection=redis_conn)
    worker.work()
