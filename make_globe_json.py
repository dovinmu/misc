## Code to convert a data per unit area grid into the .json format used by the WebGL Globe, which 
## only lists lat/lon pairs that have non-zero values.

## Currently rounds lat/lon to the nearest whole number.

fname = 'gdp90_15mi.ascii'
fname_out = 'gdp90_webglglobe_normalized.json'
start_latitude = -58
start_longitude = -180
step = .25
begin_data_idx = 6

with open(fname) as f:
    raw = f.read().strip().split('\n')

for i in range(begin_data_idx, len(raw)):
    raw[i] = raw[i].strip().split(' ')

grid = {}
curr_lat = start_latitude
curr_lon = start_longitude
for row in raw[begin_data_idx:]:
    grid[int(curr_lat)] = {}
    for el in row:
        if int(curr_lon) in grid[int(curr_lat)]:
            grid[int(curr_lat)][int(curr_lon)] += float(el)
        else:
            grid[int(curr_lat)][int(curr_lon)] = float(el)
        if float(el) > 0:
            print("{0},{1}: {2}".format(int(curr_lat), int(curr_lon), grid[int(curr_lat)][int(curr_lon)] ))
        curr_lon += step

    curr_lat += step
    curr_lon = start_longitude

max_gdp = 0
min_gdp = 0
for lat in grid.keys():
    for lon in grid[lat].keys():
        if grid[lat][lon] > max_gdp:
            max_gdp = grid[lat][lon]
        elif grid[lat][lon] < min_gdp:
            min_gdp = grid[lat][lon]

for lat in grid.keys():
    for lon in grid[lat].keys():
        if grid[lat][lon] != 0:
            grid[lat][lon] = grid[lat][lon] / max_gdp

s = '[["GDP_2025"['
for lat in grid.keys():
    for lon in grid[lat].keys():
        if grid[lat][lon] != 0:
            s += '{0},{1},{2},'.format(lat, lon, grid[lat][lon])

s = s[:-1] + ']]]'
with open(fname_out,'w') as f:
    f.write(s)





