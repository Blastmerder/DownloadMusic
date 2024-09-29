
# V1
from pydub import AudioSegment

file_name = 'K A Z I --- Skeler In My Head  K A Z I.mp3'
sound = AudioSegment.from_file(file=file_name)

if sound.dBFS < -8:
    print(sound.dBFS)
    song = sound + (-8 - sound.dBFS)
    song.export(file_name, format='mp3')
