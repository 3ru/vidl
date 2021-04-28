import shutil, youtube_dl
import moviepy.editor as mp

vn = 'aJOTlE1K90k'
ydl = youtube_dl.YoutubeDL({'outtmpl': 'tmp/%(id)s.%(ext)s', 'format': 'bestvideo, bestaudio'})
ydl.extract_info(f'https://www.youtube.com/watch?v={vn}', download=True)

#TODO 拡張子の動的取得
video = mp.VideoFileClip(f'tmp/{vn}.mp4')
video = video.set_audio(mp.AudioFileClip(f'tmp/{vn}.m4a'))
video.write_videofile(f'vid/{vn}.mp4')

shutil.rmtree('tmp/')
