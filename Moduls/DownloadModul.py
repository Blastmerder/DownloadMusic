import re
from pytubefix import YouTube


def download_video(link, path='.'):
    yt = YouTube(link)
    video = yt.streams.get_highest_resolution()
    author = re.sub(r"^[ .]|[/<>:\"\\|?*]+|[ .]$", "_", yt.author)
    title = re.sub(r"^[ .]|[/<>:\"\\|?*]+|[ .]$", "_", yt.title)

    video.download(filename=f'{path}/{author} --- {title}.mp4')
    return [f"{author} --- {title}", f"{author} - {title}"]
