
import re
import urllib.request
import urllib.error
import sys
import time
from pytube import YouTube
import os
import random

def crawl(url):
    '''
    Adapted from youParse.py Version: 1.5
    Author: pantuts
    Email: pantuts@gmail.com
    Agreement: You can use, modify, or redistribute this tool under
    the terms of GNU General Public License (GPLv3).
    This tool is for educational purposes only. Any damage you make will not affect the author.
    '''
    sTUBE = ''
    cPL = ''
    amp = 0
    final_url = []

    if 'list=' in url:
        eq = url.rfind('=') + 1
        cPL = url[eq:]

    else:
        print('Incorrect Playlist.')
        exit(1)

    try:
        yTUBE = urllib.request.urlopen(url).read()
        sTUBE = str(yTUBE)
    except urllib.error.URLError as e:
        print(e.reason)

    tmp_mat = re.compile(r'watch\?v=\S+?list=' + cPL)
    mat = re.findall(tmp_mat, sTUBE)

    if mat:
        for PL in mat:
            yPL = str(PL)
            if '&' in yPL:
                yPL_amp = yPL.index('&')
            final_url.append('http://www.youtube.com/' + yPL[:yPL_amp])

        all_url = list(set(final_url))

        i = 0
        while i < len(all_url):
            sys.stdout.write(all_url[i] + '\n')
            time.sleep(0.04)
            i = i + 1
    else:
        print('No videos found.')
        exit(1)
    return all_url


def downAll(urls, playlistName='playlist'):
    try:
        os.chdir(playlistName)
    except:
        os.mkdir(playlistName)
        os.chdir(playlistName)
    for url in urls:
        yt = YouTube(url)
        yt.get_videos()
        print('Got "{}"'.format(yt.filename))
        if len(yt.filter(resolution='480p')) == 0:
            if len(yt.filter(resolution='360p')) == 0:
                print("Can't find 480p or 360p: {}".format(yt.filename))
                continue
            video = yt.get('mp4', '360p')
        else:
            video = yt.get('mp4', '480p')
        video.download(os.getcwd())
        time.sleep(random.randint(10,20)

if len(sys.argv) < 2 or len(sys.argv) > 2:
    print('USAGE: python downYoutubeList.py YOUTUBEurl')
    exit(1)

else:
    url = sys.argv[1]
    if 'http' not in url:
        url = 'http://' + url
    urls = crawl(url)
    downAll(urls)