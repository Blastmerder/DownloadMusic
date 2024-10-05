import re
from pytubefix import YouTube
from Moduls.YouTubeModul import YouTubeData
from pytubefix import Search
from Generators.BaseElm import BaseURLVideo
from difflib import SequenceMatcher
import time
timing = time.time()


def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio() * 100


def search_video(search_name, attempts=0):
    # try search song, if can't 10 return None
    if attempts == 10:
        return None
    if True:
        print('start')
        preformat = search_name.lower()
        video_name_format = re.split(r"\s-\s", preformat) if '-' in search_name else preformat.split(
            '"') if '"' in search_name else preformat
        song_name = video_name_format[1] if len(video_name_format) == 2 else video_name_format

        authors = video_name_format[0]
        name_list_org = re.split(r"\s[\S]\s", authors)
        timing = time.time()

        s = Search(search_name)

        raw_results = s.fetch_query()

        try:
            sections = raw_results['contents']['twoColumnSearchResultsRenderer'][
                'primaryContents']['sectionListRenderer']['contents']
        except KeyError:
            sections = raw_results['onResponseReceivedCommands'][0][
                'appendContinuationItemsAction']['continuationItems']
        item_renderer = None
        for s in sections:
            if 'itemSectionRenderer' in s:
                item_renderer = s['itemSectionRenderer']

        videos = []
        if item_renderer:
            raw_video_list = item_renderer['contents']
            for video_details in raw_video_list:
                if 'videoRenderer' in video_details:
                    print(f"https://www.youtube.com/watch?v={video_details['videoRenderer']['videoId']}")
                    videos.append(
                        YouTube(f"https://www.youtube.com/watch?v={video_details['videoRenderer']['videoId']}")
                        )

        founded_video = {
            'authored': [],
            'reuploads': []
        }

        print(time.time() - timing)

        for v in videos:
            try:
                info = v.vid_info
            except:
                continue
            print(info['videoDetails'])
            # format for most speed
            url = f"https://www.youtube.com/watch?v={info['videoDetails']['videoId']}"
            # video = YouTube(url, use_oauth=True)
            title_video = info['videoDetails']['title'].lower().replace(",", "")
            author = info['videoDetails']['author']
            length = info['videoDetails']['lengthSeconds']
            thumbnail_url = info['videoDetails']['thumbnail']['thumbnails'][-1]['url']
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
