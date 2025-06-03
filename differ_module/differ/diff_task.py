import requests
import json
import difflib
db_server = "http://localhost:5010/"
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
    r = requests.get(db_server+"sources")
    if r.status_code == 404:
        j = {"name" : js["link-main"], "url" : js["link-main"]}
        requests.post(db_server+"sources")
    r = requests.get(db_server+f"documents/{js['link-main']}/{js['link']}")
    if r.status_code == 404:
        # wstaw i wyślij jako nowy
    else:
        r_json = r.json()
        diff = context_diff(js["content"], r_son["content"])
        result_str = ""
        for ele in diff:
            result_str += ele
        # wstaw i wyślij jako sprawdzony
        
        
        
    
    
    
    
    return json
