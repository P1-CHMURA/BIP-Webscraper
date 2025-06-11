from flask import Flask, request
from redis import Redis
from rq import Queue
import json
import diff_task

app = Flask(__name__)
port = 5010

db_port = 2137
db_host = "127.0.0.1"

redis_port = 6379
redis_host = "differ_redis"

queue = Queue("default", connection=Redis(host=redis_host, port=redis_port))

@app.route("/")
def index():
    return "Hello"
    
@app.route("/diff_request", methods=["POST"])
def diff_request():
    text = json.dumps(request.get_json())
    result = queue.enqueue(diff_task.DiffTask, text)
    return "Diff request processed"

if __name__ =="__main__":
	app.run(debug=True, host="0.0.0.0", port=port)
