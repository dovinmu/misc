def loadWordSet():
     s = set()
     try:
         with open('/usr/share/dict/american-english', 'r') as f:
             for line in f:
                 print(line)
                 s.add(line.strip())
    except:
        print("Sorry! This only words on a linux machine currently.")
     return s

def getPlaintext(url):
    import requests
    r = requests.get(url)
    return r.text

def snipGutenbergMetadata(text):
    print('metadata snipping not yet implemented')
    return text

def getParagraphList(text):
    result = []
    text = text.split('\n')
    temp_par = ''
    for line in text:
        if line == '\r':
            if len(temp_par) > 0:
                result.append(temp_par)
                #print(temp_par)
            temp_par = ''
            continue
        temp_par += line.strip() + ' '
    return result


def getWordList(text):
    result = []
    for par in getParagraphList(text):
        for word in par.split(' '):
            if len(word) == 0:
                continue
            for char in set('\'"1234567890-=!@#$%^&*()_+{}[]|\;:,.<>/?~`'):
                word.replace(char,'')
            result.append(word)
    return result

def findAcrostic(text, wordset, level='paragraph',min_word_len=4, max_word_len=10):
    charbuf = ''
    if level=='paragraph':
        text = getParagraphList(text)
        for i in range(len(text)):
            par = text[i]
            if par in ['\r'] or len(par) < 2:
                continue
            else:
                charbuf += par[0].lower()

            # check first n characters in the charbuf for a word, checking for largest first
            for j in range(min(len(charbuf),max_word_len), min_word_len-1, -1):
                if charbuf[:j] in wordset:
                    print(charbuf[:j].upper(), i-len(charbuf), '-', i)
                    for par_idx in range(i-len(charbuf)+1, i-len(charbuf)+j+1):
                        print(text[par_idx][0], text[par_idx][1:100]+'...', end='\n')
                    charbuf = charbuf[j:]
                    break
            if len(charbuf) > max_word_len:
                charbuf = charbuf[1:]
    if level=='word':
        text = getWordList(text)
        for i in range(len(text)):
            word = text[i]
            charbuf += word[0].lower()
            for j in range(min(len(charbuf),max_word_len), min_word_len-1, -1):
                if charbuf[:j] in wordset:
                    print(charbuf[:j].upper(), i-len(charbuf), '-', i)
                    for word_idx in range(i-len(charbuf)+1, i-len(charbuf)+j+1):
                        print(text[word_idx][0].upper() + text[word_idx][1:], end=' ')
                    print('\n')
                    charbuf = charbuf[j:]
                    break
            if len(charbuf) > max_word_len:
                charbuf = charbuf[1:]

def gutenbergAcrostic(url):
    print('processing url {}'.format(url))
    text = getPlaintext(url)
    text = snipGutenbergMetadata(text)
    print('\t\t\tparagraphs'.upper())
    findAcrostic(text, wordset, level='paragraph', min_word_len=5)
    print('\t\t\twords'.upper())
    findAcrostic(text, wordset, level='word', min_word_len=7)

if __name__ == "__main__":
    for name,url in {
        'A Christmas Carol':'http://www.gutenberg.org/cache/epub/46/pg46.txt',
        'Pride and Prejudice':'http://www.gutenberg.org/files/1342/1342-0.txt',
        "Alice's Adventures in Wonderland":'http://www.gutenberg.org/files/11/11-0.txt'
    }.items():
        print(name)
        gutenbergAcrostic(url)
