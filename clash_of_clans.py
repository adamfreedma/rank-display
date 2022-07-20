import http.client
import json


class CocPlayer:

    def __init__(self, player_tag):

        self.player_tag = player_tag
        self.api_key = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjdlMDZlZGZlLTBjMWMtNDc3My04Yzc2LTM1NDdiM2IwMTkzMyIsImlhdCI6MTY1ODIyNjAxMywic3ViIjoiZGV2ZWxvcGVyLzc2NDMyMWJhLTM4OTgtNmRlYy1iOTk0LWZjNzk3YTUwMTE0OCIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjc3LjEzNy43OC4yNTQiXSwidHlwZSI6ImNsaWVudCJ9XX0.nUd8wx1HFkxzy8RJzC4QdwgvzZPfz_-OG5xZbO6M1_7GvdIvoiNemQ8LL7JjiPX3Gb5weAgPdg2tTGlftcFFIg"

        self.data = {None}


    def update_player_data(self):

        api_key = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjdlMDZlZGZlLTBjMWMtNDc3My04Yzc2LTM1NDdiM2IwMTkzMyIsImlhdCI6MTY1ODIyNjAxMywic3ViIjoiZGV2ZWxvcGVyLzc2NDMyMWJhLTM4OTgtNmRlYy1iOTk0LWZjNzk3YTUwMTE0OCIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjc3LjEzNy43OC4yNTQiXSwidHlwZSI6ImNsaWVudCJ9XX0.nUd8wx1HFkxzy8RJzC4QdwgvzZPfz_-OG5xZbO6M1_7GvdIvoiNemQ8LL7JjiPX3Gb5weAgPdg2tTGlftcFFIg"

        header = {
            'authorization': api_key
        }

        conn = http.client.HTTPSConnection("api.clashofclans.com")

        conn.request("GET", f"/v1/players/{self.player_tag}", headers=header)

        res = conn.getresponse()
        self.data = json.loads(res.read())


    def heroes_progress(self):

        th_max_hero_sum = [0, 0, 0, 0, 0, 0, 0, 5, 10, 60, 80, 120, 170, 225, 245]

        current_th = self.get_th()

        progress = self.hero_sum() - th_max_hero_sum[current_th - 1]
        progress_traget = th_max_hero_sum[current_th] - th_max_hero_sum[current_th - 1]

        percentage = progress / progress_traget * 100

        return percentage

    get_th = lambda self : self.data["townHallLevel"]

    get_king = lambda self : self.data["heroes"][0]["level"]
    get_queen = lambda self : self.data["heroes"][1]["level"]
    get_warden = lambda self : self.data["heroes"][2]["level"]

    hero_sum = lambda self : self.get_king() + self.get_queen() + self.get_warden()