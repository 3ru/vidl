import re, requests, ffmpeg, youtube_dl, shutil, glob, moviepy.editor as mp
from settings import *


def dl(vn):
    vl = []
    os.makedirs("../DL", exist_ok=True)
    for i in ["video", "audio"]:
        ydl = youtube_dl.YoutubeDL({'outtmpl': f'../tmp/%(id)s_{i}.%(ext)s', 'format': f'best{i}'})
        ydl.extract_info(f'https://www.youtube.com/watch?v={vn}', download=True)
        vl += glob.glob(f'../tmp/{vn}_{i}*')

    _ = mp.VideoFileClip(vl[0]).set_audio(mp.AudioFileClip(vl[1])).write_videofile(f'../DL/{vn}.mp4')
    shutil.rmtree('../tmp/')
    return None


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
    resource = requests.get(URL + 'commentThreads', params=params).json()
    for comment_info in resource['items']:
        text = comment_info['snippet']['topLevelComment']['snippet']['textDisplay']
        if len(re.findall(r'\d+:\d+', text)) > 10: return text.replace('\r', '').split("\n")

    return None


def get_time_comment(lst):
    times, comments = [], []
    if lst is not None:
        for i in lst:
            if time := re.findall(r'\d+.*:\d+', i):
                n = re.search(r'\d+.*:\d+', i).end()
                times.append(*time)
                comments.append(i[n:].replace(' ', ''))
                print(*time, i[n:].replace(' ', ''))
    return times, comments


def splitter(vn, time_list, comment_list):
    secs, stream = [], ffmpeg.input(f'../DL/{vn}.mp4')
    os.makedirs(f'../FIN/{vn}', exist_ok=True)

    for i in time_list:
        if len(t := i.split(':')) > 2: secs.append((int(t[0]) * 60 + int(t[1])) * 60 + int(t[2]))
        elif len(t := i.split(':')) == 2: secs.append(int(t[0]) * 60 + int(t[1]))

    for i, s in enumerate(secs):
        trim = ffmpeg.output(stream, f'../FIN/{vn}/{comment_list[i][:10]}.mp4', ss=s, t=secs[i + 1] - s)
        thumb = ffmpeg.filter(stream, 'select', f'gte(n,{30 * (s + 1)})').output(
            f'../FIN/{vn}/{comment_list[i][:10]}_thumbnail.jpg',
            vframes=1, format='image2',
            vcodec='mjpeg')
        ffmpeg.run(trim)
        ffmpeg.run(thumb)
        if i == len(secs) - 2: break
    os.rename(f'../FIN/{vn}', f'../FIN/[済]-{vn}')

    return None


def _init():
    url = input("動画URLを入力: ")
    if e := re.search(r'\?v=', url): vn = url[e.end():]
    else: return print("正常なURLを入力してください")

    try: dl(vn)
    except Exception as e: return print(f'動画DLにてエラーが発生しました\n{e}')

    try: times, comments = get_time_comment(get_comment(vn))
    except Exception as e: return print(f'YouTubeコメント取得してエラーが発生しました\n{e}')

    try: splitter(vn, times, comments)
    except Exception as e: return print(f'動画分割にてエラーが発生しました\n{e}')
    print("\n処理が完了しました")


if __name__ == '__main__':
    _init()