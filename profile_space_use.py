import os

folderSizeCache = {}
def getFolderSize(folder):
    '''Get the size in bytes of the given directory.

    Adapted from this Stack Overflow question:
    http://stackoverflow.com/questions/1392413/calculating-a-directory-size-using-python'''
    global folderSizeCache

    total_size = os.path.getsize(folder)

    try:
        os.listdir(folder)
    except:
        print('Unable to recurse on {0}'.format(folder))
        return total_size
    for item in os.listdir(folder):
        itempath = os.path.join(folder, item)
        if os.path.isfile(itempath):
            total_size += os.path.getsize(itempath)
        elif os.path.isdir(itempath):
            if itempath in folderSizeCache:
                size = folderSizeCache[itempath]
            else:
                size = getFolderSize(itempath)
                folderSizeCache[itempath] = size
            total_size += size
    folderSizeCache[folder] = total_size
    return total_size

def prettifyCurrentDir(current, curr_size, itempath):
    for i in range(len(current)):
        if len(current[i]) > 13:
            current[i] = current[i][:7] + '...' + current[i][-3:]
    current.insert(0, itempath)
    current.insert(0, '{} mb'.format(int(curr_size/1000000)))
    current = ', '.join(current)
    if len(current) > 85:
        current = current[:85] + '...'
    return current

def getListOfBlocks(folder):
    '''Return a list of lists of files and subdirectories in the given folder that all total approximately 1gb.'''
    minimum = 10**9
    maximum = 2*minimum

    result = []
    current = []
    curr_size = 0

    try:
        os.listdir(folder)
    except:
        print('Skipping {}'.format(folder))
        return []
    for item in os.listdir(folder):
        itempath = os.path.join(folder, item)
        if os.path.isfile(itempath):
            size = os.path.getsize(itempath)
            if curr_size + size > maximum:
                if curr_size > 10**8:
                    current = prettifyCurrentDir(current, curr_size, folder)
                    result.append(current)
                current = []
                curr_size = 0
            current.append(item)
            curr_size += size
            if curr_size > minimum:
                current = prettifyCurrentDir(current, curr_size, folder)
                result.append(current)
                current = []
                curr_size = 0
        elif os.path.isdir(itempath):
            size = getFolderSize(itempath)
            if size > maximum:
                temp = getListOfBlocks(itempath)
                result.extend(temp)
                current = [temp[-1]]
            elif size > minimum:
                current.extend([item])
                curr_size += size
                current = prettifyCurrentDir(current, curr_size, folder)
                result.append(current)
                current = []
                curr_size = 0
            else:
                current.append(item)
                curr_size += size
                if curr_size > minimum:
                    current = prettifyCurrentDir(current, curr_size, folder)
                    result.append(current)
                    current = []
                    curr_size = 0
    if curr_size > 10**8:
        current = prettifyCurrentDir(current, curr_size, folder)
        result.append(current)
    return result

def profileSpace(folder):
    '''Get the total size of the given folder, as well as a breakdown of
    the contents into 1gb chunks.'''
    size = getFolderSize(folder)
    blocks = getListOfBlocks(folder)
    print('\n\t{0}: {1} gb'.format(folder, int(size/1000000)/1000))
    print('\n'.join(blocks))

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        folder = sys.argv[1]
    else:
        folder = os.getcwd()
    profileSpace(folder)
