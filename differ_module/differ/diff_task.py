import requests


def DiffTask():
    r = requests.get("http://localhost:5010/")
    print(r)
    return r
