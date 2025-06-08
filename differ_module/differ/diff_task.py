import requests
import json
import difflib
db_server = "http://localhost:5010/"

def sendToLLM(source, name, typ, text, timestamp, status):
    js = {}
    js["source"] = source
    js["name"] = name
    js["typ"] = typ
    js["content"] = text
    js["timestamp"] = timestamp
    js["status"] = status
    #wyślij do LLM

def DiffTask(text):
    #r = requests.get("http://localhost:5010/")
    js = json.loads(text)
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
    typ = js["type"]
    content = js["content"]
    timestamp = js["timestamp"]
    j = {"name" : link_main, "url" : link_main}
    r = requests.post(db_server+"sources", j)
    j = {"name" : link_main}
    r = requests.post(db_server+f"documents/{link_main}", j)
    
    r = requests.get(db_server+"/documents_latest/"+link)
    
    # sprawdz czy jest jakaś wersja tego dokumentu
    if r.status_code == 404:
        error_msg = r.content["error"]
        if error_msg.startswith("Nie"):
            j = {}
            j["name"] = link
            data["typ"] = typ
            r = requests.post(db_server+f"documents/{link_main}", j)
            j2 = {}
            j2["content"] = content
            j2["timestamp"] = timestamp
            requests.post(db_server+f"versions/{link}", j2)
            sendToLLM(link_main, link, typ, content, timestamp, "NEW")
        if error_msg.startswith("Brak"):
            j = {}
            j["content"] = content
            j["timestamp"] = timestamp
            requests.post(db_server+f"versions/{link}", j)
            sendToLLM(link_main, link, typ, content, timestamp, "NEW")
    else:
        r_json = r.json()
        diff = context_diff(content, r_json["content"])
        result_str = ""
        if len(list(diff)) == 0:
            return
        for ele in diff:
            result_str += ele
        j = {}
        j["content"] = result_str
        j["timestamp"] = timestamp
        requests.post(db_server+f"versions/{link}", j)
        sendToLLM(link_main, link, typ, content, timestamp, "UPDATE")

    return json
