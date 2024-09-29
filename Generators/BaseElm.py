from pytubefix import YouTube


class BaseURLVideo:
    def __init__(self, url: str, similarity: float | int = 100, thumbnail_url: str = None, author: str = None, title: str = None,
                 length: int = None, searched_name: str = None):
        self.url = url
        video = None if thumbnail_url is not None and author is not None and title is not None and length is not None\
            else YouTube(self.url)
        self.thumbnail_url = video.thumbnail_url if thumbnail_url is None else thumbnail_url
        self.author = video.author if author is None else author
        self.title = video.title if title is None else title
        self.length = length if length is not None else video.length
        self.similarity = similarity
        self.searched_name = searched_name if searched_name is not None else f'{self.author} - {self.title}'
