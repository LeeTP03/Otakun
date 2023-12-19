from jikanpy import Jikan
import json


class JikanAPI:
    def __init__(self) -> None:
        self.jikan = Jikan()

    def get_by_title(self, title):
        anime = self.jikan.search(search_type="anime", query=title, parameters={"limit": 1})
        with open("jikanOutput.json", "w") as f:
            json.dump(anime, f, indent=4)

    def get_anime(self, id):
        pass


class Anime:
    def __init__(self) -> None:
        pass


j = JikanAPI()
j.get_by_title("horimiya")
