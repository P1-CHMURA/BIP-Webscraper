from redis import Redis
from rq import Worker

# Preload libraries
import diff_task

# Provide the worker with the list of queues (str) to listen to.
w = Worker(['default'], connection=Redis(host="127.0.0.1", port=5011))
w.work()
