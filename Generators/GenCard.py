import dearpygui.dearpygui as dpg
from Generators.BaseElm import BaseURLVideo
import webbrowser
from urllib.request import urlretrieve
from Moduls.CropModul import crop
import os
from Moduls.GlobalDownloadModul import download
import re
from threading import Thread


class Cards:
    def __init__(self, urls: list[dict[str, list[BaseURLVideo]]], texture_reg: dpg.texture_registry,
                 path_to_download: str, load_ind: dpg.window, dialog_err: dpg.window):

        self.path_dir = path_to_download
        self.load_ind = load_ind
        self.dialog_err = dialog_err

        self.urls = urls
        self.keys_usage = [{'from': 'authored', 'index': 0}]

        try:
            dpg.delete_item(item='Cards')
        except:
            pass

        # create all windows

        # main
        self.window = dpg.add_window(tag='Cards')
        dpg.set_primary_window(self.window, True)

        # file dialog
        self.file_dialog = dpg.add_file_dialog(
            directory_selector=True,
            show=False,
            callback=self.__pre_downloading,
            width=700,
            height=400,
            default_path=path_to_download,
            modal=True
        )

        # setting card window
        self.window_base_setting = dpg.add_window(
            no_resize=True,
            no_close=True,
            show=False,
            width=300,
            height=200
        )
        self.__default_settings()

        self.height_window = 360
        self.texture_reg = texture_reg

        self.keys_usage = [{'from': 'authored', 'index': -1} if i['authored'] else {'from': 'reuploads', 'index': -1}
                           for i in urls]

        self.__draw_cards()

    def __default_settings(self):
        dpg.add_button(
            label='Ok',
            parent=self.window_base_setting,
            pos=(5, 175),
            callback=self.__apply_settings
        )
        dpg.add_button(
            label='Cancel',
            parent=self.window_base_setting,
            pos=(35, 175),
            callback=lambda: dpg.hide_item(self.window_base_setting)
        )

    def __apply_settings(self):
        dpg.hide_item(self.window_base_setting)

    def __pre_downloading(self, sender, app_data, user_data):
        self.path_dir = app_data['current_path']

        download(user_data['url'], self.path_dir, self.load_ind, self.dialog_err)
        
    def __start_download(self, url, index):
        err = download(url, self.path_dir, self.load_ind, self.dialog_err)
        if not err:
            self.__del_card(index)

    def add_card(self, track: str | dict[str, list[BaseURLVideo]]):
        if type(track) is str:
            if track != '':
                new_card = {
                    "authored": [BaseURLVideo(track)],
                    "reuploads": []
                }
                self.urls.append(new_card)
            self.keys_usage.append({'from': 'authored', 'index': -1})
            self.__draw_cards()
        else:
            self.keys_usage.append({'from': 'authored', 'index': -1})
            self.urls.append(track)
            self.__draw_cards()

    def __get_base_data(self, index):
        if self.urls[index]["authored"]:
            similarity = self.urls[index]["authored"][-1].similarity
            author = self.urls[index]["authored"][-1].author
            title = self.urls[index]["authored"][-1].title
            search_name = self.urls[index]["authored"][-1].searched_name
            thumbnail_url = self.urls[index]["authored"][-1].thumbnail_url
        else:
            if self.urls[index]["reuploads"]:
                similarity = self.urls[index]["reuploads"][-1].similarity
                author = self.urls[index]["reuploads"][-1].author
                title = self.urls[index]["reuploads"][-1].title
                search_name = self.urls[index]["reuploads"][-1].searched_name
                thumbnail_url = self.urls[index]["reuploads"][-1].thumbnail_url
            else:
                author = 'null'
                title = 'null'
                similarity = 0
                search_name = 'null'
                thumbnail_url = None

        output_data = {
            'author': author,
            'title': title,
            'similarity': similarity,
            'search_name': search_name,
            'thumbnail_url': thumbnail_url
        }

        return output_data

    def __draw_cards(self):
        dpg.delete_item(item=self.window, children_only=True)

        for index in range(len(self.urls)):
            pos_x = (index % 5) * 210 + 20
            pos_y = (index // 5) * self.height_window + 40

            self.__draw_card(index=index, pos=(pos_x, pos_y))

    def __del_card(self, card_index):
        del self.urls[card_index]
        del self.keys_usage[card_index]
        self.__draw_cards()

    def __create_modal(self, button):
        with dpg.popup(button, mousebutton=dpg.mvMouseButton_Left, modal=True) as sett:
            dpg.add_button(label="Close", callback=lambda: dpg.configure_item(sett, show=False))

    def __draw_buttons(self, index: int, parent):
        if self.urls[index]["authored"]:
            link = self.urls[index]["authored"][-1].url
        else:
            link = self.urls[index]["reuploads"][-1].url if \
                self.urls[index]["reuploads"] else 'https://www.youtube.com/'

        floppy = dpg.add_image_button(
            texture_tag='floppy.png',
            pos=(165, 195),
            tint_color=(25, 239, 44, 255),
            parent=parent,
            callback=lambda: self.__start_download(link, index)
        )

        yt = dpg.add_image_button(
            texture_tag='youtube.png',
            pos=(135, 195),
            tint_color=(255, 50, 50, 255),
            parent=parent,
            callback=lambda: webbrowser.open(link)
        )

        settings = dpg.add_image_button(
            texture_tag='sliders2.png',
            pos=(105, 195),
            parent=parent
        )

        self.__create_modal(settings)

        trash = dpg.add_image_button(
            texture_tag='trash.png',
            pos=(5, 195),
            callback=lambda: self.__del_card(index),
            tint_color=(239, 25, 25, 255),
            parent=parent
        )

        with dpg.tooltip(floppy):
            dpg.add_text("Download Only This Video.")
        with dpg.tooltip(yt):
            dpg.add_text("Go To The Video.")
        with dpg.tooltip(trash):
            dpg.add_text("Delete Card.")
        with dpg.tooltip(settings):
            dpg.add_text("Settings Downloading.")

    def __draw_card(self, index: int, pos: tuple[int, int]):
        with dpg.child_window(pos=pos, width=195, height=self.height_window, parent=self.window) as win:
            self.__draw_buttons(index, win)

            try:
                base_elm = self.urls[index][self.keys_usage[index]['from']][self.keys_usage[index]['index']]
                author = base_elm.author
                title = base_elm.title
                similarity = base_elm.similarity
                search_name = base_elm.searched_name
                thumbnail_url = base_elm.thumbnail_url
            except:
                author = 'null'
                title = 'null'
                similarity = 0
                search_name = 'null'
                thumbnail_url = None

            name = re.sub(
               r"^[ .]|[/<>:\"\\|?*]+|[ .]$", "_", f'{author} - {title}')
            if not os.path.exists('tmp/raw'):
                os.mkdir('tmp/raw')
            if not os.path.exists('tmp/crops'):
                os.mkdir('tmp/crops')

            if not os.path.exists(f'tmp/raw/{name}.jpg'):
                urlretrieve(thumbnail_url, f'tmp/raw/{name}.jpg')
            if not os.path.exists(f'tmp/crops/{name}.jpg'):
                crop(f'tmp/raw/{name}.jpg', f'tmp/crops/{name}.jpg')

            try:
                width, height, channels, data = dpg.load_image(f'tmp/crops/{name}.jpg')
            except: ...

            try:
                dpg.add_static_texture(width=width, height=height, default_value=data,
                                       tag=name, parent=self.texture_reg)
            except:
                pass

            try:
                dpg.add_image(name, width=180, height=180)
            except:
                pass

            with dpg.child_window(pos=(5, 220)):
                with dpg.child_window(height=55, menubar=True, border=False):
                    with dpg.menu_bar():
                        dpg.add_text('Author', pos=(60, 0))
                    dpg.add_text(author)
                with dpg.child_window(menubar=True, border=False):
                    with dpg.menu_bar():
                        dpg.add_text('Song', pos=(65, 0))
                    dpg.add_text(title)
            color_tint = (255, 50, 50, 255) if similarity < 75 else (25, 239, 44, 255)

            inf = dpg.add_image(texture_tag="info-circle.png", pos=(10, 10), tint_color=color_tint)
            with dpg.tooltip(inf):
                dpg.add_text(f'Similarity: {similarity}', color=color_tint)
                dpg.add_text(f"Search Name: {search_name}", wrap=100, color=color_tint)

    def __len__(self):
        return len(self.urls)

    @property
    def videos(self):
        return [i[self.keys_usage[self.urls.index(i)]['from']][self.keys_usage[self.urls.index(i)]['index']].url
                for i in self.urls]
