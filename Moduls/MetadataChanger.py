import music_tag
import moviepy.editor as mp
import os


def change_metadata_sound(name, format_audio='mp3', sound_folder='', picture_path: str = None,
                          author: str = None, title: str = None):
    if os.path.exists(f'{sound_folder}/{name}.{format_audio}'):
        # Normalize volume
        sound = mp.AudioFileClip(f"{sound_folder}/{name}.{format_audio}")
        sound.write_audiofile(f"{sound_folder}/{name}_.{format_audio}")

        os.remove(f"{sound_folder}/{name}.{format_audio}")
        os.rename(f"{sound_folder}/{name}_.{format_audio}", f"{sound_folder}/{name}.{format_audio}")

        f = music_tag.load_file(f"{sound_folder}/{name}.{format_audio}")

        # Add MetaData
        f['title'] = name.split(' --- ')[1] if title is None else title
        f['artist'] = name.split(' --- ')[0] if author is None else author

        if picture_path is None:
            raise FileNotFoundError
        else:
            with open(f'{picture_path}', 'rb') as img_in:
                f['artwork'] = img_in.read()
            with open(f'{picture_path}', 'rb') as img_in:
                f.append_tag('artwork', img_in.read())

        f.save()
    else:
        raise FileNotFoundError
