import http.client
import json

def get_rank(name, tag):

    conn = http.client.HTTPSConnection("api.henrikdev.xyz")

    conn.request("GET", f"/valorant/v1/mmr/eu/{name}/{tag}",)

    res = conn.getresponse()
    data = json.loads(res.read())
    
    return data["data"]["currenttierpatched"]
