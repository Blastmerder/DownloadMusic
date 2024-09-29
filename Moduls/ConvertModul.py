import moviepy.editor as mp
import music_tag
import os
from pydub import AudioSegment


def convert_video_to_audio(name, format_audio='mp3', format_video='mp4', folder_tmp='tmp', result_folder='',
                           folder_video='', picture_path: str = None):
    if os.path.exists(f'{folder_video}/{name}.{format_video}'):
        clip = mp.VideoFileClip(f"{folder_video}/{name}.{format_video}")
        clip.audio.write_audiofile(f"{result_folder}/{name}.{format_audio}")

        if not os.path.exists(folder_tmp):
            os.mkdir(folder_tmp)

        if picture_path is None:
            clip.save_frame(f'{folder_tmp}/{name}.png', 30)

        # Normalize volume
        sound = AudioSegment.from_file(file=f'{result_folder}/{name}.mp3')

        if sound.dBFS < -8:
            song = sound + (-8 - sound.dBFS)
            song.export(f"{result_folder}/{name}.mp3", format='mp3')

        f = music_tag.load_file(f"{result_folder}/{name}.mp3")

        f['title'] = name.split(' --- ')[1]
        f['artist'] = name.split(' --- ')[0]

        if picture_path is None:
            with open(f'{folder_tmp}/{name}.png', 'rb') as img_in:
                f['artwork'] = img_in.read()
            with open(f'{folder_tmp}/{name}.png', 'rb') as img_in:
                f.append_tag('artwork', img_in.read())
        else:
            with open(f'{picture_path}', 'rb') as img_in:
                f['artwork'] = img_in.read()
            with open(f'{picture_path}', 'rb') as img_in:
                f.append_tag('artwork', img_in.read())

        f.save()
        clip.close()

        if os.path.exists(f'{folder_tmp}/{name}.png'):
            os.remove(f'{folder_tmp}/{name}.png')
        os.remove(f'{folder_video}/{name}.{format_video}')
    else:
        raise "File doesn't exist"
