import http.client
import json
import numpy as np


def get_rank(player_id, playlist=None):
    """returns a player's rocket league rank

    Args:
        player_id (str): a player's epic ID, can be found in epic games website
        playlist (str, optional): the specific rocket league playlist to check the rank of. Defaults to None.

    Returns:
        str: the player's rank
    """
    conn = http.client.HTTPSConnection("rocket-league1.p.rapidapi.com")

    headers = {
        'X-RapidAPI-Key': "8e72018a94msh4c3262c98201d33p111978jsn41062226b314",
        'X-RapidAPI-Host': "rocket-league1.p.rapidapi.com"
    }

    conn.request("GET", f"/ranks/{player_id}", headers=headers)

    res = conn.getresponse()
    data = json.loads(res.read())

    if playlist:
        for mode in data["ranks"]:
            if mode["playlist"] == playlist:
                return mode["rank"]
    
    # if no playlist was entered or the playlist entered dose not exist, pick the best playlist
    max_mmr = 0
    max_rank = ""
    # iterating through all playlists to find the best one
    for mode in data["ranks"]:
        if mode["mmr"] > max_mmr:
            max_mmr = mode["mmr"]
            max_rank = mode["rank"]

    return max_rank