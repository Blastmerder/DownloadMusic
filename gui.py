import json
import dearpygui.dearpygui as dpg
from pytubefix import YouTube
import re
from threading import Thread
from Generators.GenCard import Cards
from Moduls.SearchModul import search_video
from Moduls.GlobalDownloadModul import download
import webbrowser

from Moduls.base_functions import update_textures

URL_VIDEO_SEARCH = ''
URLS = []
# video = YouTube('https://www.youtube.com/watch?v=NaM6Ik9DW8o&t=54s', use_oauth=True)


def callback(sender, app_data):
    with open('./settings/settings.json', 'r+') as settings:
        file = json.load(settings)

        file['current_path'] = app_data['current_path']
        global path_to_download
        path_to_download = app_data['current_path']

        settings.seek(0)
        json.dump(file, settings, indent=4)
        settings.truncate()

        dpg.delete_item(sender)
        dpg.add_file_dialog(directory_selector=True, show=False, callback=callback, tag="file_dialog_id", width=700,
                            height=400,
                            default_path=path_to_download)

        dpg.set_item_label('default_path', path_to_download)


def start_search(URL):
    video = YouTube(URL)
    description = ''
    for n in range(6):
        try:
            description = video.initial_data["engagementPanels"][n]["engagementPanelSectionListRenderer"]["content"][
                "structuredDescriptionContentRenderer"]["items"][1]["expandableVideoDescriptionBodyRenderer"][
                "attributedDescriptionBodyText"]["content"]
        except:
            continue

    # found in the description time codes

    time_codes = re.finditer(r"\d{2}:\d{2}\s*.\s*(.+)", fr'{description}', re.MULTILINE)

    names_sounds = []

    # add to the names sounds list all songs from time codes
    for matchNum, match in enumerate(time_codes, start=1):
        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1
            names_sounds.append(match.group(groupNum))

    threads = []

    def search(video_list):
        for video in video_list:
            result_url = search_video(video) if video is not None else None
            if result_url:
                cards.add_card(result_url)

            del result_url

    videos = [names_sounds[i:i + 2] for i in range(0, len(names_sounds), 2)]

    if names_sounds is not None and len(names_sounds) > 4:
        for i in range(len(videos)):
            twrv = Thread(target=search, args=(videos[i],))
            threads.append(twrv)
            twrv.start()

        for t in threads:
            t.join()


def set_global_url_video(sender):
    global URL_VIDEO_SEARCH
    URL_VIDEO_SEARCH = dpg.get_value(sender)


def download_all_songs():
    for video in cards.videos:
        download(video, path_to_download, load_ind, dialog_err)


dpg.create_context()
dpg.create_viewport(
    title='Downloader Music',
    width=1270,
    height=720,
    small_icon=r'textures\DM.ico',
    large_icon=r'textures\DM.ico'
)

with open('./settings/settings.json', 'r+') as settings:
    file = json.load(settings)
    path_to_download = file['current_path']

with dpg.texture_registry(show=False) as texture_reg: ...

with dpg.window(no_close=True, no_title_bar=True, show=False,
                pos=(dpg.get_viewport_width()//2, dpg.get_viewport_height()//2)) as load_ind:
    dpg.add_loading_indicator(style=1)
    dpg.add_text('Status Now: ')

with dpg.window(no_close=True, no_title_bar=True, show=False,
                pos=(dpg.get_viewport_width()//2, dpg.get_viewport_height()//2)) as dialog_err:
    dpg.add_text("Completed successfully!")
    dpg.add_button(label="Close", callback=lambda: dpg.hide_item(dialog_err))


dpg.add_file_dialog(directory_selector=True, show=False, callback=callback, tag="file_dialog_id", width=700, height=400,
                    default_path=path_to_download, modal=True)


update_textures(texture_reg)

# Menu Bar
with dpg.viewport_menu_bar() as bar:
    input_txt2 = dpg.add_input_text(callback=set_global_url_video, hint="https://www.youtube.com/watch?v=")
    search = dpg.add_image_button(
        label="Search",
        enabled=True,
        callback=lambda: start_search(URL_VIDEO_SEARCH),
        texture_tag='search.png'
    )

    git = dpg.add_image_button(
        texture_tag='github.png',
        callback=lambda: webbrowser.open('https://github.com/Blastmerder'),
        pos=(dpg.get_viewport_width()-40, 0)
    )
    settings = dpg.add_image_button(
        enabled=True,
        texture_tag='sliders2.png',
        pos=(dpg.get_viewport_width()-dpg.get_item_width(git)*3-50, 0)
    )

    with dpg.popup(settings, mousebutton=dpg.mvMouseButton_Left, modal=True):
        path = dpg.add_button(label=path_to_download, callback=lambda: dpg.show_item("file_dialog_id"),
                              tag='default_path')

    with dpg.menu(label="Other"):
        # Work with all cards
        with dpg.menu(label="For Cards"):
            download_all = dpg.add_image_button(
                enabled=True,
                callback=download_all_songs,
                texture_tag='download.png'
            )

        # Work with URL
        with dpg.menu(label="Single One/URL"):
            with dpg.group(horizontal=True):
                card = dpg.add_image_button(
                    texture_tag='file-earmark-plus.png',
                    callback=lambda: cards.add_card(URL_VIDEO_SEARCH)
                )
                download_single = dpg.add_image_button(
                    enabled=True,
                    callback=lambda: download(URL_VIDEO_SEARCH, path_to_download, load_ind, dialog_err, True),
                    texture_tag='download.png'
                )

    # ToolTips
    with dpg.tooltip(download_single):
        dpg.add_text("Download It Video And Convert.")

    with dpg.tooltip(card):
        dpg.add_text("Add Card From URL.")

    with dpg.tooltip(download_all):
        dpg.add_text("Download All Video From Card.")

    with dpg.tooltip(git):
        dpg.add_text("Go To Git Project.")

    with dpg.tooltip(input_txt2):
        dpg.add_text("URL For Video Download/Searching.")

    with dpg.tooltip(search):
        dpg.add_text("Start Searching All Songs From Video.")

node_list = {}
cards = Cards(URLS, texture_reg, path_to_download, load_ind, dialog_err)

dpg.setup_dearpygui()
dpg.show_viewport()
# dpg.set_primary_window("Primary Window", True)
# dpg.start_dearpygui()

while dpg.is_dearpygui_running():
    # insert here any code you would like to run in the render loop
    # you can manually stop by using stop_dearpygui()

    dpg.set_item_pos(
        git,
        pos=[dpg.get_viewport_width()-dpg.get_item_width(git)*3, 0]
    )
    dpg.set_item_pos(
        settings,
        pos=[dpg.get_viewport_width()-dpg.get_item_width(git)*3-dpg.get_item_width(settings)-10, 0]
    )

    dpg.render_dearpygui_frame()


dpg.destroy_context()
