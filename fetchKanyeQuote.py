import requests

def getKanye():
    response = requests.get("https://api.kanye.rest/").json()
    return response['quote']