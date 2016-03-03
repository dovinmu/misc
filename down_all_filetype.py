from bs4 import BeautifulSoup, SoupStrainer
import requests

FILETYPE = '.mp3'
URL = 'http://dataskeptic.com/episodes.php'
FILTER = 'MINI' #make an empty string for no filter

def down_all_filetype(URL, FILETYPE, FILTER):
    r = requests.get(URL)
    soup = BeautifulSoup(r)
    strainer = SoupStrainer('a') #this filters everything except links, called 'tags' in Soup parlance

    for tag in soup.find_all(strainer):
        link = tag['href']
        if FILETYPE in link and FILTER in link:
            r = requests.get(link)
            print('Got %s' % link)
            with open(link.split('/')[-1], 'wb') as f: #write out the bytes with the same filename as
                f.write(r.content)                     #the original


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 1:
        print('''
        Usage:
            down_all_filetype.py <url> <filetype> [filter]
        ''')
    else:
        FILETYPE = sys.argv[2]
        URL = sys.argv[1]
        if len(sys.argv) == 4:
            FILTER = sys.argv[3]
        else:
            FILTER = ''
        down_all_filetype(URL, FILETYPE, FILTER)
