import re, requests, ffmpeg, youtube_dl, shutil, glob
from src.settings import *
import moviepy.editor as mp


def dl(vn):
    vl = []
    os.makedirs("../DL", exist_ok=True)
    for i in ["video", "audio"]:
        ydl = youtube_dl.YoutubeDL({'outtmpl': f'../tmp/%(id)s_{i}.%(ext)s', 'format': f'best{i}'})
        ydl.extract_info(f'https://www.youtube.com/watch?v={vn}', download=True)
        vl += glob.glob(f'../tmp/{vn}_{i}*')

    video = mp.VideoFileClip(vl[0])
    video = video.set_audio(mp.AudioFileClip(vl[1]))
    video.write_videofile(f'../DL/{vn}.mp4')

    # shutil.rmtree('./tmp/')


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


def splitter(vn, time_list, comment_list):
    secs = []
    os.makedirs(vn, exist_ok=True)

    for i in time_list:
        if len(t := i.split(':')) > 2:
            secs.append((int(t[0]) * 60 + int(t[1])) * 60 + int(t[2]))
        elif len(t := i.split(':')) == 2:
            secs.append(int(t[0]) * 60 + int(t[1]))

    stream = ffmpeg.input(f'../DL/{vn}.mp4')
    for i, s in enumerate(secs):
        trim = ffmpeg.output(stream, f'../{vn}/{comment_list[i][:10]}.mp4', ss=s, t=secs[i + 1] - s)
        thumb = ffmpeg.filter(stream, 'select', f'gte(n,{30 * (s + 1)})').output(f'../{vn}/{comment_list[i][:10]}.jpg',
                                                                                 vframes=1, format='image2',
                                                                                 vcodec='mjpeg')
        ffmpeg.run(trim)
        ffmpeg.run(thumb)
        if i == len(secs) - 2:
            break
    os.rename(f'../{vn}', f'../[済]-{vn}')

    return None


vid = "DC6JppqHkaM"

dl(vid)
# times, comments = get_time_comment(get_comment(vid))
# splitter(vid, times, comments)
