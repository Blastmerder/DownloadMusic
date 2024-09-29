import re
from pytubefix import YouTube
from Moduls.YouTubeModul import YouTubeData
from pytubefix import Search
from Generators.BaseElm import BaseURLVideo
from difflib import SequenceMatcher


def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio() * 100


def search_video(search_name, attempts=0):
    # try search song, if can't 10 return None
    if attempts == 10:
        return None
    if True:
        preformat = search_name.lower()

        video_name_format = re.split(r"\s-\s", preformat) if '-' in search_name else preformat.split(
            '"') if '"' in search_name else preformat
        song_name = video_name_format[1] if len(video_name_format) == 2 else video_name_format

        authors = video_name_format[0]
        name_list_org = re.split(r"\s[\S]\s", authors)

        s = Search(search_name)

        videos = [v for v in s.videos]

        founded_video = {
            'authored': [],
            'reuploads': []
        }

        for v in videos:
            # format for most speed
            url = v.watch_url
            # video = YouTube(url, use_oauth=True)
            title_video = v.title.lower().replace(",", "")
            author = v.author
            length = v.length
            thumbnail_url = v.thumbnail_url
            have_author = False

            # Is it true author or not
            name_authors_list = author.lower()
            name_list = re.split(r"\s[\S]\s", name_authors_list)

            for name in name_list:
                if name in name_list_org:
                    have_author = True

            if have_author and length > 60:
                # formate name video ( author / name song )
                name = re.split(r"\s-\s", title_video)

                name_video_alt = title_video.split('"')[1] if '"' in title_video else None

                # get max similarity with search name and title video ( video been named with name author or not)
                similarity1 = similarity(title_video, song_name)
                similarity2 = similarity(name[1], song_name) if len(name) == 2 else 0
                similarity3 = similarity(name_video_alt, song_name) if name_video_alt else 0
                similarity4 = similarity(name[0], song_name) if len(name) == 2 else 0

                result = BaseURLVideo(
                    url=url,
                    title=title_video,
                    similarity=max(similarity1, similarity2, similarity3, similarity4),
                    length=length,
                    thumbnail_url=thumbnail_url,
                    author=author,
                    searched_name=search_name
                )

                founded_video['authored'].append(result)
            else:
                if length > 60:
                    result = BaseURLVideo(
                        url=url,
                        title=title_video,
                        similarity=similarity(title_video.replace('"', ''), song_name),
                        length=length,
                        thumbnail_url=thumbnail_url,
                        author=author,
                        searched_name=search_name
                    )

                    founded_video['reuploads'].append(result)

        founded_video['authored'].sort(key=lambda x: x.similarity)
        founded_video['reuploads'].sort(key=lambda x: x.similarity)

        return founded_video
        """except:
        # Try again
        attempts += 1
        search_video(search_name, attempts=attempts)"""
