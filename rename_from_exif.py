# script to rename .jpg files in the folder to dates
import exifread
import os
from datetime import datetime

dates = {}
for fname in [fname for fname in os.listdir() if fname[-4:].lower() == '.jpg']:
    f = open(fname, 'rb')
    tags = exifread.process_file(f)
    if 'EXIF DateTimeOriginal' not in tags:
        print('Could not get metadata on file {}'.format(fname))
        continue
    dtag = tags['EXIF DateTimeOriginal']
    
    taken_list = [int(i) for i in dtag.values.split(' ')[0].split(':')]
    taken_dtime = datetime(*taken_list)
    fout_name = taken_dtime.strftime('%Y-%B-%d')
    if taken_dtime in dates:
        dates[taken_dtime].append(fname)
        fout_name += '_' + str(len(dates[taken_dtime]))
    else:
        dates[taken_dtime] = [fname]
    os.rename(fname, fout_name + '.jpg')
    print("renamed {0} to {1}".format(fname, fout_name + '.jpg'))
