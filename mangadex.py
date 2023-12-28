import requests
import json


class MangaDexAPI:
    def __init__(self):
        self.api_url = "https://api.mangadex.org"

    def get_manga(self, arg, limit=3):
        order = {"relevance": "desc"}
        final_order_query = {}
        languages = ["en"]

        query_manga_id = []
        query_manga = []

        for key, value in order.items():
            final_order_query[f"order[{key}]"] = value

        response = requests.get(
            f"{self.api_url}/manga",
            params={"title": arg, "limit": limit, **final_order_query},
        )

        if response.json()["total"] == 0:
            return "No results found"

        for item in response.json()["data"]:
            query_manga_id.append(item["id"])

        for id in query_manga_id:
            data = requests.get(
                f"{self.api_url}/manga/{id}?includes[]=author&includes[]=artist&includes[]=cover_art"
            )
            query_manga.append(Manga(data.json()["data"]))
        
        return query_manga


class Manga:
    def __init__(self, data) -> None:
        self.data = data
        self.api_url = "https://api.mangadex.org"
        self.init_data()

    def init_data(self):
        m_attributes = self.data["attributes"]
        m_relationships = self.data["relationships"]

        self.id = self.data["id"]
        self.title = m_attributes["title"]["en"]
        self.description = m_attributes["description"]["en"] if "en" in m_attributes["description"] else ""
        self.chapter_number = "N/A" if m_attributes["lastChapter"] == "" else m_attributes["lastChapter"]
        self.volume_number = "N/A" if m_attributes["lastVolume"] == "" else m_attributes["lastVolume"]
        self.status = m_attributes["status"]
        self.demographic = m_attributes["publicationDemographic"]
        self.tags = []
        
        languages = ["en"]
        latest_chapter_response = requests.get(
            f"{self.api_url}/manga/{self.id}/feed",
            params={
                "translatedLanguage[]": languages,
                "limit": "25",
                "order[volume]": "desc",
                "order[chapter]": "desc",
            },
        )

        self.all_chapters = []
        
        if latest_chapter_response.json()["data"] == []:
            self.latest_chapter_id = "No Chapters Found"
        else:
            self.latest_chapter_id = latest_chapter_response.json()["data"][0]["id"]
            self.all_chapter_ids = [[i["id"], i["attributes"]["title"], i["attributes"]["chapter"]] for i in latest_chapter_response.json()["data"]]

        for i in m_attributes["tags"]:
            self.tags.append(i["attributes"]["name"]["en"])

        for info in m_relationships:
            if info["type"] == "author":
                self.author = info["attributes"]["name"]
                self.author_twitter = info["attributes"]["twitter"]
            if info["type"] == "cover_art":
                self.cover_id = info["id"]
                self.cover_filename = info["attributes"]["fileName"]
    
    def get_manga_feed(self):
        for i in self.all_chapter_ids:
            self.all_chapters.append(Chapter(self.title, i[0], i[1], i[2], self.latest_chapter_link))
    
    def get_latest_link(self):
        
        if self.latest_chapter_id == "No Chapters Found":
            return ["No Chapters Found", "No Chapters Found", "No Chapters Found"]
        
        r = requests.get(f"{self.api_url}/chapter/{self.latest_chapter_id}")
        if r.json()["data"]["attributes"]["externalUrl"] == None:
            self.latest_chapter_link = f"https://mangadex.org/chapter/{self.latest_chapter_id}"
            return [
                f"https://mangadex.org/chapter/{self.latest_chapter_id}",
                r.json()["data"]["attributes"]["title"],
                r.json()["data"]["attributes"]["chapter"],
            ]
        else:
            self.latest_chapter_link = r.json()["data"]["attributes"]["externalUrl"]
            return [
                r.json()["data"]["attributes"]["externalUrl"],
                r.json()["data"]["attributes"]["title"],
                r.json()["data"]["attributes"]["chapter"],
            ]
            
    def get_cover(self):
        return f"https://fxmangadex.org/covers/{self.id}/{self.cover_filename}"

    def get_manga_site(self):
        title_name = self.title.replace(" ", "-")
        return f"https://mangadex.org/title/{self.id}/{title_name}"

    def get_tags(self):
        res = ""
        for i in self.tags:
            res += i + ", "
        return res[:-2]

    def get_status(self):
        return self.status.capitalize()

    def get_demographic(self):
        if self.demographic == None:
            return "N/A"
        return self.demographic.capitalize()

    def __str__(self):
        return f"Title: {self.title}\nID: {self.id}\nDescription: {self.description}\nCover ID: {self.cover_id}\nCover Filename: {self.cover_filename}"

class Chapter:
    def __init__(
        self,
        manga_title,
        chapter_id: str,
        chapter_title: str = None,
        chapter_number: str = None,
        chapter_link: str = None,
    ) -> None:
        self.manga_title = manga_title
        self.chapter_id = chapter_id
        self.hash = ""
        self.base_url = ""
        self.data = []
        self.result = ""
        self.chapter_title = chapter_title
        self.chapter_number = chapter_number
        self.chapter_link = chapter_link

    def get_data(self):
        r = requests.get(f"https://api.mangadex.org/at-home/server/{self.chapter_id}")
        with open("output.json", "w") as f:
            json.dump(r.json(), f, indent=4)
        self.result = r.json()["result"]

        if self.result == "error":
            return "Error"

        if r.json()["chapter"]["dataSaver"] == []:
            self.result = "error"
            return "Error"

        self.hash = r.json()["chapter"]["hash"]
        self.base_url = r.json()["baseUrl"]
        self.data = r.json()["chapter"]["dataSaver"]
        return self.get_pages()

    def get_pages(self):
        page_url = []
        for page in self.data:
            init_url = f"{self.base_url}/data-saver/{self.hash}/{page}"
            page_url.append(init_url.replace("https://uploads.mangadex.org/data-saver/", "https://fxmangadex.org/data-saver/"))
        return page_url


if __name__ == "__main__":
    m = MangaDexAPI()
    s = m.get_manga("Jujutsu Kaisen")
