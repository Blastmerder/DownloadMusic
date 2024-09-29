from os.path import isfile, join
from os import listdir
from Moduls.ConvertModul import convert_video_to_audio
from Moduls.DownloadModul import download_video


# ссылка на загружаемое видео
link = "https://www.youtube.com/watch?v=iXOBbvdO0o4"
download_video(link, path='')

video_files = [f for f in listdir(f'./music') if isfile(join(f'./music', f))]

for video_file in video_files:
    if 'mp4' in video_file:
        convert_video_to_audio(video_file.replace('.mp4', ''), folder_video=f'./music',
                               result_folder=f'./result')
