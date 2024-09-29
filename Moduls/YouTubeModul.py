import requests
from bs4 import BeautifulSoup
import json


class YouTubeData:
    def __init__(self, url):
        # creating a parsing from YT and get a body of video
        src = requests.get(url).text
        soup = BeautifulSoup(src, features='html.parser')

        body = soup.find_all('body')
        js_script = body[0].find('script').text.replace('var ytInitialPlayerResponse = ', '').replace('};', '}')

        self.__data = json.loads(js_script)

    @property
    def author(self):
        return self.__data['videoDetails']['author']

    @property
    def title(self):
        return self.__data['microformat']['playerMicroformatRenderer']['title']['simpleText']

    @property
    def thumbnail_url(self):
        return self.__data['microformat']['playerMicroformatRenderer']['thumbnail']['thumbnails'][0]['url']

    @property
    def length(self):
        return int(self.__data['microformat']['playerMicroformatRenderer']['lengthSeconds'])

    @property
    def description(self):
        return self.__data['microformat']['playerMicroformatRenderer']['description']

    @property
    def embed(self):
        return self.__data['microformat']['playerMicroformatRenderer']['embed']['iframeUrl']
