import json
import dearpygui.dearpygui as dpg
from pytubefix import YouTube
from os import listdir
from os.path import isfile, join
import re
from threading import Thread
from Generators.BaseElm import BaseURLVideo
from Generators.GenCard import Cards
from Moduls.SearchModul import search_video
import webbrowser


def update_textures(parent):
    files = [f for f in listdir(f'./textures/icons') if isfile(join(f'./textures/icons', f))]

    for file in files:
        width, height, channels, data = dpg.load_image(f'textures/icons/{file}')
        dpg.add_static_texture(width=width, height=height, default_value=data,
                               tag=file, parent=parent)