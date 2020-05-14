import os
import numpy as np
from pickle import *


'''
we have few representations ways for nodes localisation
(lat, lon) for UM 'grid nodes'
(row, col) for whole area (globalrowcol)
(row, col) only for Polans see below - the most frequent presentation in these modules (namedtuplerowcol)
'''

from collections import *
bounds = namedtuple('bounds', 'xmin xmax xlen ymin ymax ylen')
Poland = bounds(ymin=135, ymax=310, ylen=310-135, xmin=120, xmax=285, xlen=285-120)

def globalrowcol2namedtuplerowcol(rowcol, bounds):
    row, col = rowcol
    new_row, new_col = row-bounds.xmin, col-bounds.ymin
    new_rowcol = new_row, new_col
    return new_rowcol

def namedtuplerowcol2globalrowcol(rowcol, bounds):
    row, col = rowcol
    new_row, new_col = row+bounds.xmin, col+bounds.ymin
    new_rowcol = new_row, new_col
    return new_rowcol


def create_flat_latlon_map():
    rows = np.linspace(Poland.xmin, Poland.xmax-1, Poland.xlen)
    cols = np.linspace(Poland.ymin, Poland.ymax-1, Poland.ylen)
    lats = []
    lons = []
    for row in rows:
        for col in cols:
            lat, lon = um_rowcol2latlon((int(row), int(col)))
            lats.append(lat)
            lons.append(lon)
    return lats, lons


def rocol2Polandrowcol(rowcol, namedtuple0):
  return (rowcol[0]-namedtuple0.xmin, rowcol[1]-namedtuple0.ymin)

def flat_array(field):
    values = []
    for i in range(len(field)):
        for j in range(len(field[i])):
            value = field[i][j]
            values.append(value)
    return values



grid_type = "c"
comp_type = "pgrid"
directory = os.getcwd()

name1 = grid_type + '_grid'
lat_name = "".join((grid_type,'5_',comp_type,'_lats.pkl'))
lon_name = "".join((grid_type,'5_',comp_type,'_lons.pkl'))

with open(os.path.join(directory, "umimgw_proceed", "um_settings",name1,lat_name),'rb') as f:
    lat = load(f)

with open(os.path.join(directory, "umimgw_proceed", "um_settings",name1,lon_name),'rb') as f:
    lon = load(f)


def um_latlon2rowcol(latlon_point):
    lon_p = latlon_point[0]
    lat_p = latlon_point[1]
    arr = (lat-lat_p)**2 + (lon-lon_p)**2
    (row, col) = np.unravel_index(np.argmin(arr), arr.shape)
    return (row, col)


def um_rowcol2latlon(rowcol_point):
    row_p = int(rowcol_point[0])
    col_p = int(rowcol_point[1])
    return lat[row_p][col_p], lon[row_p][col_p]


def get_latlons(field, x_corner, y_corner):
    lats = []
    lons = []
    for i in range(len(field)):
        for j in range(len(field[i])):
            latt, lonn = um_rowcol2latlon([i+x_corner, j+y_corner])
            lats.append(latt)
            lons.append(lonn)

    return lons, lats

def get_latlons_ver2(field, x_corner, y_corner):
    lats = np.full_like(field, 1)
    lons = np.full_like(field, 1)
    for i in range(len(field)):
        for j in range(len(field[i])):
            latt, lonn = um_rowcol2latlon([i+x_corner, j+y_corner])
            lats[i][j] = latt
            lons[i][j] = lonn

    return lons, lats

'''
convert lat, lon to row, col localisation representation of station. lat, lon row, col are 1-dimensional and have the same shape
'''
def latlon2rowcol(lat, lon):
    row = np.array(lat)
    col = np.array(lon)
    for i in range(len(lat)):
        row[i], col[i] = um_latlon2rowcol((lat[i], lon[i]))
        row[i], col[i] = int(row[i]), int(col[i])
    return row, col


'''
convert row, col to lat, lon localisation representation of station. lat, lon row, col are 1-dimensional and have the same shape
'''
def rowcol2latlon(lat, lon):
    row = np.array(lat)
    col = np.array(lon)
    for i in range(len(lat)):
        lat[i], lon[i] = um_rowcol2latlon((row[i], col[i]))
        lat[i], lon[i] = int(lat[i]), int(lon[i])
    return lat, lon



#Tests
#print(um_latlon2rowcol((18.4843, 54.3613)))
#print(um_latlon2rowcol((17.3205, 54.4513)))
#print(um_latlon2rowcol((20.4752, 54.1425)))
#print(um_latlon2rowcol((16.2129, 53.4453)))

#print(um_rowcol2latlon((1, 2)))
#print(um_rowcol2latlon((54, 17)))
#print(um_rowcol2latlon((156, 167)))
#print(um_rowcol2latlon((300, 224)))


##TODO 3 types of grid:
# 1) PGRID - constans!
# 2) BGRID_c
# 3) BGRID_p


def make_mask(my_bounds):
    import geopandas as gpd
    from shapely.geometry import Point
    foldername = "ref-nuts-{}-{}m.shp".format(2016, "01")
    filename = "NUTS_RG_{}_{}_{}_LEVL_{}.shp".format("01M", 2016, 4326, 0)
    nf = os.path.join("nuts", foldername, filename, filename)
    with open(nf) as f:
        data = gpd.read_file(nf)

    obj = data.geometry[28]

    min_row = my_bounds.xmin
    min_col = my_bounds.ymin
    rows = range(my_bounds.xmin, my_bounds.xmax)
    cols = range(my_bounds.ymin, my_bounds.ymax)

    mask = np.array(my_bounds.xlen*my_bounds.ylen*[False]).reshape(my_bounds.xlen, my_bounds.ylen)
    for row in rows:
        for col in cols:
            coords = np.array(um_rowcol2latlon((row, col)))
            coords = np.array([coords[1], coords[0]])
            p = Point(coords)
            mask[row-min_row][col-min_col] = obj.contains(p)

    return mask

def mask2pickle(my_bounds):
    mask = make_mask(my_bounds)
    file = open("Poland_mask.pkl", "wb")
    dump((Poland, mask), file)


def pickle2mask():
    file = open(str("Poland_mask.pkl"), "rb")
    country_metadata, mask = load(file)
    return mask
