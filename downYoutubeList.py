
import re
import urllib.request
import urllib.error
import sys
import time
from pytube import YouTube
import os
import random

from downYoutubeMovie import *

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
    try:
        yTUBE = urllib.request.urlopen(url).read()
        sTUBE = str(yTUBE)
    except urllib.error.URLError as e:
        print(e.reason)

    tmp_mat = re.compile(r'watch\?v=\S+?list=' + cPL)
    mat = re.findall(tmp_mat, sTUBE)

    all_url = []
    if mat:
        for PL in mat:
            yPL = str(PL)
            if '&' in yPL:
                yPL_amp = yPL.index('&')
            final_url.append('http://www.youtube.com/' + yPL[:yPL_amp])

        all_url.append(final_url.pop(0))
        while final_url:
            el = final_url.pop(0)
            if all_url[-1] != el:
                all_url.append(el)

        i = 0
        while i < len(all_url):
            #yt = YouTube(all_url[i])
            #sys.stdout.write(yt.filename + ', ' + all_url[i] + '\n')
            sys.stdout.write(all_url[i] + '\n')
            time.sleep(0.04)
            i = i + 1
    else:
        print('No videos found.')
    return all_url

def downAll(urls, playlistName='playlist', skippable=False, ftype=None, mask=None):
    try:
        os.chdir(playlistName)
    except:
        os.mkdir(playlistName)
        os.chdir(playlistName)
    if not mask:
        mask = '1'
    if len(mask) < len(urls):
        el = mask[-1]
        mask = mask + el * (len(urls) - len(mask))
    for i in range(len(urls)):
        url = urls[i]
        if mask[i] == '1':
            down(url, skippable=skippable, ftype=filetype)
            time.sleep(random.randint(3,10))


if len(sys.argv) < 2 or len(sys.argv) > 4:
    print('USAGE: python downYoutubeList.py YOUTUBEurl [-s: skippable] [-f: <filetype:mp3>] [-mask: <bitstring>]')
else:
    url = sys.argv[1]
    if 'http' not in url:
        url = 'http://' + url
    if '-s' in sys.argv:
        skippable = True
    else:
        skippable = False
    if '-f' in sys.argv:
        filetype = sys.argv[sys.argv.index('-f')+1]
    else:
        filetype = None
    if '-mask' in sys.argv:
        mask = sys.argv[sys.argv.index('-mask')+1]
    else:
        mask = None
    urls = crawl(url)
    downAll(urls, ftype=filetype, skippable=skippable, mask=mask)
