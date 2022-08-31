import http.client
import json
from os import kill


class ValorantPlayer:

    def __init__(self, name, tag):

        self.name = name
        self.tag = tag
        self.prev_matchID = ""


    def get_rank(self):
        """returns a player's valorant rank

        Args:
            name (str): player's name
            tag (str): player's tag

        Returns:
            str: player's rank
        """
        conn = http.client.HTTPSConnection("api.henrikdev.xyz")

        conn.request("GET", f"/valorant/v1/mmr/eu/{self.name}/{self.tag}",)

        res = conn.getresponse()
        data = json.loads(res.read())
        
        
        try:
            return data["data"]["currenttierpatched"]
        except Exception:
            return None

    def _get_game_stats(self):
        """returns the player's last valorant match stats

        Args:
            name (str): player's name
            tag (str): player's tag
            prev_matchID (str): last match id

        Returns:
            bool, str: has a match occurred, player's kda
        """
        conn = http.client.HTTPSConnection("api.henrikdev.xyz")

        conn.request("GET", f"/valorant/v3/matches/eu/{self.name}/{self.tag}",)

        res = conn.getresponse()
        data = json.loads(res.read())
        
        try:
            last_match = data["data"][0]
            metadata =  last_match["metadata"]

            if metadata["matchid"] == self.prev_matchID:
                return False, -1

            self.prev_matchID = metadata["matchid"]
            
            all_players = last_match["players"]["all_players"]

            for player in all_players:
                if player["name"] == self.name and player["tag"] == self.tag:
                    curr_player = player

            return True, curr_player["stats"]
        except Exception:
            return False, -1

    def get_kda(self):

        ret, player_stats = self._get_game_stats()

        if not ret:
            return False, -1

        return True, round(player_stats["kills"] / player_stats["deaths"], 1)

