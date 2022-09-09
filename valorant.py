import http.client
import json
from os import kill


class ValorantPlayer:

    def __init__(self, name, tag):

        self.name = name
        self.tag = tag
        self.prev_matchID = ""

        self.match_data = {}
        self.new_game = False


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
        except KeyError:
            return None

    def update_match_stats(self):
        """update the player's valorant match history stats

        Args:
            name (str): player's name
            tag (str): player's tag
            prev_matchID (str): last match id

        Returns:
            bool, str: has a match occurred, player's kda
        """
        if self.match_data:
            self.prev_matchID = self.match_data[0]["metadata"]["matchid"]


        conn = http.client.HTTPSConnection("api.henrikdev.xyz")

        conn.request("GET", f"/valorant/v3/matches/eu/{self.name}/{self.tag}",)

        res = conn.getresponse()
        data = json.loads(res.read())

        try:        
            self.match_data = data["data"]

            self.new_game = self.match_data[0]["metadata"]["matchid"] != self.prev_matchID
        except KeyError:
            print(data)
            pass

    def _get_player(self, match_id=0):
        """gets the player stats on a match

        Args:
            match_id (int): the match how many matches ago, (0 -> 0 match ago, 2 -> 2 matches ago)

        Returns:
            dictionary: player
        """
        try:
            tracked_match = self.match_data[match_id]
            metadata =  tracked_match["metadata"]

            all_players = tracked_match["players"]["all_players"]

            for player in all_players:
                if player["name"] == self.name and player["tag"] == self.tag:
                    curr_player = player

            return curr_player
        except KeyError:
            return False, -1

    def get_kda(self):
        player = self._get_player()

        player_stats = player["stats"]

        return round(player_stats["kills"] / player_stats["deaths"], 1)

    def get_win(self, match_id=0):
        """gets if the player won on a match

        Args:
            match_id (int): the match how many matches ago, (0 -> 0 match ago, 2 -> 2 matches ago)

        Returns:
            bool: did he win
        """

        player = self._get_player()

        player_team = player["team"].lower()

        return bool(self.match_data[match_id]["teams"][player_team]["has_won"])

