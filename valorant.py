import http.client
import json

def get_rank(name, tag):
    """returns a player's valorant rank

    Args:
        name (str): player's name
        tag (str): player's tag

    Returns:
        str: player's rank
    """
    conn = http.client.HTTPSConnection("api.henrikdev.xyz")

    conn.request("GET", f"/valorant/v1/mmr/eu/{name}/{tag}",)

    res = conn.getresponse()
    data = json.loads(res.read())
    
    return data["data"]["currenttierpatched"]
