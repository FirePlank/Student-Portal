from youtubesearchpython import SearchVideos
import json


class YoutubeSearch:
    def __init__(self, keyword):
        self.keyword = keyword
        self.result = json.loads(SearchVideos(self.keyword, offset=1, mode="json", max_results=10).result())["search_result"]

    def links(self):
        links = []
        for i in self.result:
            links.append(i["link"])
        return links

    def titles(self):
        titles = []
        for i in self.result:
            titles.append(i["title"])
        return titles

    def channels(self):
        channels = []
        for i in self.result:
            channels.append(i["channel"])
        return channels

    def durations(self):
        durations = []
        for i in self.result:
            durations.append(i["duration"])
        return durations

    def views(self):
        views = []
        for i in self.result:
            views.append(i["views"])
        return views

    def thumbnails(self):
        thumbnails = []
        for i in self.result:
            thumbnails.append(i["thumbnails"][0])
        return thumbnails

    def all(self):
        everything=[]
        for i in self.result:
            everything.append([i["channel"], i["title"], i["link"], i["duration"], i["views"], i["thumbnails"][0]])
        return everything