import re
from pytubefix import YouTube
from pytubefix import request
from urllib.error import HTTPError
from threading import Thread, Timer


def download_video(link, path='.'):
    yt = YouTube(link)
    video = yt.streams.get_audio_only()
    author = re.sub(r"^[ .]|[/<>:\"\\|?*]+|[ .]$", "_", yt.author)
    title = re.sub(r"^[ .]|[/<>:\"\\|?*]+|[ .]$", "_", yt.title)

    # video.download(filename=f'{path}/{author} --- {title}', mp3=True)
    file_path = f'{path}/{author} --- {title}.mp3'
    bytes_remaining = video.filesize
    timeout = 60
    max_retries = 0

    stop = False

    def stop_process():
        global stop
        stop = True
        raise TimeoutError

    timer = Timer(60, stop_process)
    timer.start()

    with open(file_path, "wb") as fh:
        try:
            for chunk in request.stream(
                    video.url,
                    timeout=timeout,
                    max_retries=max_retries
            ):
                if stop:
                    break
                # reduce the (bytes) remainder by the length of the chunk.
                bytes_remaining -= len(chunk)
                # send to the on_progress callback.
                video.on_progress(chunk, fh, bytes_remaining)
        except HTTPError as e:
            if e.code != 404:
                raise
        except StopIteration:
            # Some adaptive streams need to be requested with sequence numbers
            for chunk in request.seq_stream(
                    video.url,
                    timeout=timeout,
                    max_retries=max_retries
            ):
                if stop:
                    break
                # reduce the (bytes) remainder by the length of the chunk.
                bytes_remaining -= len(chunk)
                # send to the on_progress callback.
                video.on_progress(chunk, fh, bytes_remaining)

    video.on_complete(file_path)
    timer.cancel()

    return [f"{author} --- {title}", f"{author} - {title}"] if not stop else False
