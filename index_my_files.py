import os
import sys
import json


dirs_visited = 0

def index_subdirs(rel_dir, depth=0):
    if rel_dir == '':
        return
    os.chdir(rel_dir)
    subdirs = [x for x in next(os.walk('.'))[1] if x[0] != '.']
    subdirs = sorted(subdirs)
    print('\n', os.getcwd(), '\n', '\t' * depth, os.listdir())
    for sd in subdirs:
        if sd not in skips:
            index_subdirs(sd, depth+1)
    global dirs_visited
    dirs_visited += 1
    os.chdir('..')


if 'indexer_data.json' in os.listdir():
    with open('indexer_data.json') as f:
        j = json.loads(f.read())
        os.chdir(j['dir'])
        skips = j['relativeSkips']
        top_level_skips = j['topLevelSkips']
else:
    skips = []
    top_level_skips = []

if __name__ == '__main__':
    if len(sys.argv) > 1:
        os.chdir(sys.argv[1])
    index_subdirs('.')
