import os, youtube_dl
import moviepy.editor as mp

vn = 'aJOTlE1K90k'
ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s', 'format': 'bestvideo, bestaudio'})
url = f'https://www.youtube.com/watch?v={vn}'
with ydl:
    ydl.extract_info(
        url,
        download=True
    )

video = mp.VideoFileClip(f'{vn}.webm')
video = video.set_audio(mp.AudioFileClip(f'{vn}.m4a'))
video.write_videofile(f'{vn}.mp4')

for i in ['.webm', '.m4a']:
    os.remove(vn + i)
