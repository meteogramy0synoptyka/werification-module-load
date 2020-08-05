

# PARAMS for um and IMGW ###
import os
import json
from sys import *
from datetime import datetime, timedelta, timezone
from get_umimgw import *

# liczba DÓB do ściągnięcia:
len_series = 2
imgw_stations = "all"
# tzinfo - ważne !!!
# start = datetime(2010, 1, 1, 0, tzinfo=timezone.utc)
start = datetime(2018, 4, 1, 0, tzinfo=timezone.utc)

nodes = loadImgwRowcolNodes()

stations = loadImgwCodesStations()

typeParameter = "ground"

# case1
# UM-IMGW pair
for node in nodes:
    mongo_load_imgw_series(start, node, len=len_series *
                           24, param=code_imgw_ground_temp_5)
    mongo_load_um_series(start, node, len_series,
                         param=code_um_ground_temp, onlyZerosStarts=false)

# case2
# download only IMGW datas
# for (i, station) in enumerate(stations[11:]):
#     mongoLoadImgwStationsSeries(start, i, station, len=len_series*24)

# case3 - only UM
# for node in nodes:
#     mongo_load_um_series(start, node, len_series, param="ground")
