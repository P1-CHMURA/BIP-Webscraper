import requests
import json
import difflib
db_server = "http://postgres_api:5011/"
llm_server = "http://llm:5020/summarize"
headers={
    'Content-type':'application/json', 
    'Accept':'application/json'
}
def sendToLLM(source, name, typ, text, timestamp, status):
    js = {}
    js["source"] = source
    js["name"] = name
    js["typ"] = typ
    js["content"] = text
    js["timestamp"] = timestamp
    js["status"] = status
    r = requests.post(llm_server, json = js, headers = headers)

def DiffTask(text):    
    js = json.loads(text)[0]
    if 'link-main' not in js:
        return "error"
    if 'link' not in js:
        return "error"
    if 'content' not in js:
        return "error"
    if 'typ' not in js:
        return "error"
    if 'timestamp' not in js:
        return "error"
    link_main = js["link-main"]
    link = js["link"]
    typ = js["typ"]
    content = js["content"]
    timestamp = js["timestamp"]
    j = {"name" : link_main}
    r = requests.post(db_server+"sources", json = j, headers = headers)
    j = {"name" : link, "typ" : typ}
    
    r = requests.post(db_server+f"documents/{link_main}", json = j, headers = headers)
    
    r = requests.get(db_server+"/documents_latest/"+link)
    if r.status_code == 404:
        j = {}
        j["content"] = content
        j["timestamp"] = timestamp
        requests.post(db_server+f"versions/{link}", json = j, headers = headers)
        sendToLLM(link_main, link, typ, content, timestamp, "NEW")
    else:
        r_json = r.json()
        diff = difflib.context_diff(r_json["content"], content)
        result_str = ""
        for ele in diff:
            result_str = result_str + ele
        if result_str=="":
            return
        j = {}
        j["content"] = content
        j["timestamp"] = timestamp
        requests.post(db_server+f"versions/{link}", json = j, headers = headers)
        sendToLLM(link_main, link, typ, result_str, timestamp, "UPDATE")
