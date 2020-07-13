

# PARAMS for um and IMGW ###
import os
import json
from sys import *
from datetime import datetime, timedelta, timezone
from get_umimgw import *

len_series = 4
imgw_stations = "all"
# tzinfo - ważne !!!
start = datetime(2010, 1, 1, 0, tzinfo=timezone.utc)

nodes = load_imgw_rowcol_nodes()
print(nodes)

for node in nodes:
    mongo_load_faster_sequence_single_point(start, node, len=len_series*24)
    mongo_load_um_series(start, node, len_series)
