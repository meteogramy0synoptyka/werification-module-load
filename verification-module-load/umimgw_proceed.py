

# PARAMS for um and IMGW ###
import os
import json
from sys import *
from datetime import datetime, timedelta
from get_umimgw import *

len_series = 365*10
imgw_stations = "all"
start = datetime(2010, 1, 1, 0)

NODES = [
    #(row, col)
    (175, 162)  # kotlina jeleniogórska
    # (264, 280),  # okolice suwałk
    # (281, 195),  # łeba forest
    # (281, 196),  # łeba urban
    # (255, 268)   # jeziora (Poligon woskowy ORZYSZ)
]

for node in NODES:
    mongo_load_um_series(start, node, len_series)
    mongo_load_faster_sequence_single_point(
        start, node, len=len_series*24)
