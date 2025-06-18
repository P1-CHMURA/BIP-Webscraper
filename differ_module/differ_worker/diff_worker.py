from redis import Redis
from rq import Worker

# Preload libraries
import diff_task

# Provide the worker with the list of queues (str) to listen to.
w = Worker(['default'], connection=Redis(host="differ_redis", port=6379))

w.work()
