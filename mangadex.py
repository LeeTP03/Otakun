import requests
import json


class MangaDexAPI:
    def __init__(self):
        self.api_url = "https://api.mangadex.org"
        self.headers = {"Content-Type": "application/json"}
        self.params = {"limit": 10}
        self.search_url = "https://api.mangadex.org/manga"
        self.search_params = {"title": ""}
        self.search_headers = {"Content-Type": "application/json"}

    def get_manga(self, arg):
        order = {"rating": "desc", "followedCount": "desc"}
        final_order_query = {}
        languages = ["en"]
        chapter_order = {
            "createdAt": "asc",
            "updatedAt": "asc",
            "publishAt": "asc",
            "readableAt": "asc",
            "volume": "asc",
            "chapter": "asc",
        }

        for key, value in order.items():
            final_order_query[f"order[{key}]"] = value

        self.search_params["title"] = arg
        response = requests.get(
            f"{self.api_url}/manga", params={"title": arg, **final_order_query}
        )

        if response.json()["total"] == 0:
            return "No results found"

        single_response = requests.get(
            f"{self.api_url}/manga/{response.json()['data'][0]['id']}?includes[]=author&includes[]=artist&includes[]=cover_art"
        )

        latest_chapter_response = requests.get(
            f"{self.api_url}/manga/{response.json()['data'][0]['id']}/feed",
            params={
                "translatedLanguage[]": languages,
                "limit": "1",
                "order[createdAt]": "desc",
                "order[volume]": "desc",
                "order[chapter]": "desc",
                "order[updatedAt]": "desc",
                "order[publishAt]": "desc",
                "order[readableAt]": "desc",
            },
        )
        newest_chapter = latest_chapter_response.json()["data"][0]["id"]
        res_manga = self.initialise_manga(single_response, newest_chapter)
        return res_manga

    def initialise_manga(self, response, latest_chapter):
        m_attributes = response.json()["data"]["attributes"]
        m_relationships = response.json()["data"]["relationships"]

        m_title = m_attributes["title"]["en"]
        m_id = response.json()["data"]["id"]
        m_description = m_attributes["description"]["en"]
        m_chapter_number = m_attributes["lastChapter"]
        m_volume_number = m_attributes["lastVolume"]
        m_status = m_attributes["status"]
        m_demographic = m_attributes["publicationDemographic"]
        m_tags = []
        m_latest_chapter = self.get_latest_link(latest_chapter)
        m_latest_chapter_id = latest_chapter

        for i in m_attributes["tags"]:
            m_tags.append(i["attributes"]["name"]["en"])

        for info in m_relationships:
            if info["type"] == "author":
                m_author = info["attributes"]["name"]
                m_author_twitter = info["attributes"]["twitter"]
            if info["type"] == "cover_art":
                m_cover_id = info["id"]
                m_cover_filename = info["attributes"]["fileName"]

        m = Manga(
            m_title,
            m_id,
            m_description,
            m_cover_id,
            m_cover_filename,
            m_chapter_number,
            m_volume_number,
            m_author,
            m_author_twitter,
            m_status,
            m_demographic,
            m_tags,
            m_latest_chapter,
            m_latest_chapter_id,
        )
        return m

    def get_latest_link(self, id):
        r = requests.get(f"{self.api_url}/chapter/{id}")
        if r.json()["data"]["attributes"]["externalUrl"] == None:
            return f"https://mangadex.org/chapter/{id}"
        else:
            return r.json()["data"]["attributes"]["externalUrl"]


class Manga:
    def __init__(
        self,
        title,
        id,
        description,
        cover_id,
        cover_filename,
        chapter_number,
        volume_number,
        author,
        author_twitter,
        status,
        demographic,
        tags,
        latest_chapter,
        latest_chapter_id,
    ):
        self.title = title
        self.id = id
        self.description = description
        self.cover_id = cover_id
        self.cover_filename = cover_filename
        self.number_of_chapters = "N/A" if chapter_number == "" else chapter_number
        self.number_of_volumes = "N/A" if volume_number == "" else volume_number
        self.author = author
        self.author_twitter = author_twitter
        self.status = status
        self.demographic = demographic
        self.tags = tags
        self.latest_chapter = latest_chapter
        self.latest_chapter_id = latest_chapter_id

    def get_cover(self):
        return f"https://fxmangadex.org/covers/{self.id}/{self.cover_filename}"

    def get_manga_site(self):
        title_name = self.title.replace(" ", "-")
        return f"https://mangadex.org/title/{self.id}/{title_name}"

    def get_chapter_pages(self):
        c = Chapter(self.latest_chapter_id)
        return c.get_pages()

    def get_tags(self):
        res = ""
        for i in self.tags:
            res += i + ", "
        return res[:-2]

    def get_status(self):
        return self.status.capitalize()

    def get_demographic(self):
        return self.demographic.capitalize()

    def __str__(self):
        return f"Title: {self.title}\nID: {self.id}\nDescription: {self.description}\nCover ID: {self.cover_id}\nCover Filename: {self.cover_filename}"


class Chapter:
    def __init__(self, chapter_id: str) -> None:
        self.chapter_id = chapter_id
        self.hash = ""
        self.base_url = ""
        self.data = []
        self.result = ""
        self.get_data()

    def get_data(self):
        r = requests.get(f"https://api.mangadex.org/at-home/server/{self.chapter_id}")
        with open("output.json", "w") as f:
            json.dump(r.json(), f, indent=4)
        self.result = r.json()["result"]
        
        if self.result == "error":
            return
        
        self.hash = r.json()["chapter"]["hash"]
        self.base_url = r.json()["baseUrl"]
        self.data = r.json()["chapter"]["dataSaver"]

    def get_pages(self):
        if self.result == "error":
            return ["Error"]
        page_url = []
        for page in self.data:
            page_url.append(f"{self.base_url}/data-saver/{self.hash}/{page}")
        return page_url


if __name__ == "__main__":
    m = MangaDexAPI()
    s = m.get_manga("one piece")
    print(s.get_chapter_pages())
