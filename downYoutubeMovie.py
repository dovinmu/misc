import os
import sys
import time
from pytube import YouTube

def down(url, directory):
    yt = YouTube(url)
    yt.get_videos()
    print('Found "{}"'.format(yt.filename))
    if len(yt.filter(resolution='480p')) == 0:
        if len(yt.filter(resolution='360p')) == 0:
            print("Can't find 480p or 360p: {}".format(yt.filename))
            return
        video = yt.get('mp4', '360p')
    else:
        video = yt.get('mp4', '480p')
    video.download(os.getcwd())
    print('...download finished')

if len(sys.argv) < 2 or len(sys.argv) > 3:
    print('USAGE: python downYoutubeMovie.py YOUTUBEurl [/full/directory/name]')
    exit(1)
else:
    url = sys.argv[1]
    if 'http' not in url:
        url = 'http://' + url
    if len(sys.argv) > 2:
        directory = sys.argv[2]
    else:
        directory = os.getcwd()
    down(url, directory)
