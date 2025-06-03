from flask import Flask, request
from redis import Redis
from rq import Queue
import json
import diff_task

app = Flask(__name__)
port = 5010

db_port = 2137
db_host = "127.0.0.1"

redis_port = 5011
redis_host = "127.0.0.1"

queue = Queue("default", connection=Redis(host=redis_host, port=redis_port))
@app.route("/")
def index():
    print("hello")
    return "Hello"
    
@app.route("/diff_request", methods=["POST"])
def diff_request():
    text = "{\"link-main\": \"https://dupa.pl\",\"link\": \"https://dupa.pl/zasób\",\"content\": \"cały zescrapowany tekst\",\"typ\": \"pdf\", \"timestamp\": \"jakiś czas\"}";
    
    
    result = queue.enqueue(diff_task.DiffTask, text)
    return "diff request processed"

if __name__ =="__main__":
	app.run(debug=True, port=port)
