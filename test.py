import requests
import json
BASE = "http://127.0.0.1:5000/player"

myObject =   {"FIDE":{"standard": 1300, "rapid": None, "blitz":None},
        "USCF":{"regular": None, "quick": None, "blitz": None},
        "Chesscom":{"bullet":None, "blitz":None, "rapid":None, "daily":None, "puzzle":None},
        "LiChess":{"bullet":None, "blitz":None, "rapid":None, "classical":None, "correspondence":None, "training":None}}

response = requests.post(BASE, myObject)
print(response.json())