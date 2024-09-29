import re
from pytubefix import YouTube


def download_video(link, path='.'):
    yt = YouTube(link)
    video = yt.streams.get_audio_only()
    author = re.sub(r"^[ .]|[/<>:\"\\|?*]+|[ .]$", "_", yt.author)
    title = re.sub(r"^[ .]|[/<>:\"\\|?*]+|[ .]$", "_", yt.title)

    video.download(filename=f'{path}/{author} --- {title}', mp3=True)
    return [f"{author} --- {title}", f"{author} - {title}"]
