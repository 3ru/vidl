import re, requests, json, shutil, youtube_dl
import moviepy.editor as mp
from settings import AK


def ytdl(vn=''):
    ydl = youtube_dl.YoutubeDL({'outtmpl': 'tmp/%(id)s.%(ext)s', 'format': 'bestvideo, bestaudio'})
    ydl.extract_info(f'https://www.youtube.com/watch?v={vn}', download=True)

    # TODO 拡張子の動的取得
    video = mp.VideoFileClip(f'tmp/{vn}.mp4')
    video = video.set_audio(mp.AudioFileClip(f'tmp/{vn}.m4a'))
    video.write_videofile(f'vid/{vn}.mp4')

    shutil.rmtree('tmp/')


def get_comment(video_id, n=30):
    URL = 'https://www.googleapis.com/youtube/v3/'
    params = {
        'key': AK,
        'part': 'snippet',
        'videoId': video_id,
        'order': 'relevance',
        'textFormat': 'plaintext',
        'maxResults': n,
    }
    response = requests.get(URL + 'commentThreads', params=params)
    resource = response.json()

    for comment_info in resource['items']:
        text = comment_info['snippet']['topLevelComment']['snippet']['textDisplay']
        if len(re.findall(r'\d+:\d+', text)) > 10:
            return text.replace('\r', '').split("\n")

    return None


def get_time_comment(lst):
    times, comments = [], []
    if lst is not None:
        for i in lst:
            if time := re.findall(r'\d+.*:\d+', i):
                n = re.search(r'\d+.*:\d+', i).end()
                times.append(*time)
                comments.append(i[n:].replace(' ', ''))
    return times, comments


res1, res2 = get_time_comment(get_comment(f'{id}'))
