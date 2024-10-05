import re
from threading import Thread, Timer
from pytubefix import YouTube
from Moduls.DownloadModul import download_video
from Moduls.ConvertModul import convert_video_to_audio
from Moduls.MetadataChanger import change_metadata_sound
import dearpygui.dearpygui as dpg
import os
from os.path import isfile, join
from os import listdir
from urllib.request import urlretrieve
from Moduls.CropModul import crop
import requests


def download_image(url, save_as):
    response = requests.get(url)
    with open(save_as, 'wb') as file:
        file.write(response.content)


def run_in_thread(fn):
    def run(*k, **kw):
        t = Thread(target=fn, args=k, kwargs=kw)
        t.start()
        return t

    return run


def check_raw_videos():
    if not os.path.exists('./tmp/RawVideos'):
        os.mkdir('./tmp/RawVideos')
    else:
        directory = './tmp/RawVideos'
        for filename in os.listdir(directory):
            filename = re.sub(r"^[ .]|[/<>:\"\\|?*]+|[ .]$", "_", filename)
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)


def get_data(link):
    yt = YouTube(link)
    try:
        author = re.sub(r"^[ .]|[/<>:\"\\|?*]+|[ .]$", "_", yt.author)
        title = re.sub(r"^[ .]|[/<>:\"\\|?*]+|[ .]$", "_", yt.title)
    except:
        author = yt.author
        title = yt.title
    return [f"{author} --- {title}", f"{author} - {title}", yt.thumbnail_url, {'author': yt.author, 'title': yt.title}]


def error_print():
    raise TimeoutError


def download(url, path_download, load_ind, dialog_err, download_pict=False):
    try:
        if not os.path.exists('tmp/raw'):
            os.mkdir('tmp/raw')
        if not os.path.exists('tmp/crops'):
            os.mkdir('tmp/crops')

        dpg.set_value(dpg.get_item_children(load_ind)[1][1], "Status Now: \nInit")
        dpg.show_item(load_ind)
        # check existing videos
        # check_raw_videos()
        name_video, name_image, thumbnail_url, metadata = get_data(url)

        if not os.path.exists(f'{path_download}/{name_video}.mp3'):
            dpg.set_value(dpg.get_item_children(load_ind)[1][1], "Status Now: \nDownload Audio")
            download_video(url, path_download)

        if download_pict:
            if not os.path.exists(f'tmp/raw/{name_image}.jpg'):
                # download_image(thumbnail_url, f'tmp/raw/{name_image}.jpg')
                urlretrieve(thumbnail_url, f'tmp/raw/{name_image}.jpg')
            if not os.path.exists(f'tmp/crops/{name_image}.jpg'):
                crop(f'tmp/raw/{name_image}.jpg', f'tmp/crops/{name_image}.jpg')

        if (os.path.exists(f'{path_download}/{name_video}.mp3') and
                not os.path.getsize(f'{path_download}/{name_video}.mp3')):
            os.remove(f'{path_download}/{name_video}.mp3')
            raise FileNotFoundError
        dpg.set_value(dpg.get_item_children(load_ind)[1][1], "Status Now: \nChange Metadata")

        change_metadata_sound(
            name=name_video,
            picture_path=f'./tmp/crops/{name_image}.jpg',
            author=metadata['author'],
            title=metadata['title'],
            sound_folder=path_download
        )
        error = None
    except BaseException as err:
        error = err
        print(err)
        download(url, path_download, load_ind, dialog_err, download_pict)
    except Exception as err:
        error = err

    dpg.hide_item(load_ind)
    dpg.set_value(dpg.get_item_children(load_ind)[1][1], "Status Now: \nInit")
    dpg.show_item(dialog_err)
    if error and error != '':
        dpg.set_value(dpg.get_item_children(dialog_err)[1][0], f"ERROR: \n{error}")
    else:
        dpg.set_value(dpg.get_item_children(dialog_err)[1][0], f"Completed Successfully")
    return error
