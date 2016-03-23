import os
import sys
import time
from pytube import YouTube

def down(url, directory=None, skippable=False):
    if not directory:
        directory = os.getcwd()
    try:
        yt = YouTube(url)
    except:
        print('Could not get URL "{}"'.format(url))
        return
    yt.get_videos()
    print('Found "{}"'.format(yt.filename))
    if skippable and input("Download? [y]/n: ") != '':
        return
    if len(yt.filter(resolution='480p')) == 0:
        if len(yt.filter(resolution='360p')) == 0:
            print("Can't find 480p or 360p: {}".format(yt.filename))
            return
        video = yt.get('mp4', '360p')
    else:
        video = yt.get('mp4', '480p')
    try:
        video.download(os.getcwd())
        print('...download finished')
    except OSError:
        print("Could not write file")

if len(sys.argv) < 2 or len(sys.argv) > 3:
    print('USAGE: python downYoutubeMovie.py YOUTUBEurl [/full/directory/name]')
else:
    url = sys.argv[1]
    if 'http' not in url:
        url = 'http://' + url
    if len(sys.argv) > 2:
        directory = sys.argv[2]
    else:
        directory = os.getcwd()
    down(url, directory)
