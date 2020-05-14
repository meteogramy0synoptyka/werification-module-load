

# PARAMS for um and IMGW ###
import os
import json
from sys import *
from datetime import datetime, timedelta
from get_umimgw import *

len_series = int(argv[1])
node = (int(argv[2]), int(argv[3]))  # (264, 280)
imgw_stations = "all"
anticipation = 0
start = datetime.strptime(argv[4], "%Y-%m-%dT%H")  # 2016-3-5T0

um_series = load_um_series(start, anticipation, len_series)
imgw_series = load_faster_sequence_single_point(start, node, len=len_series)


js = {"start": argv[4], "len_series": len_series, "row": node[0], "col": node[1], "stations": imgw_stations,
      "anticipation": anticipation, "um": um_series,  "imgw": imgw_series}


jsonobj = json.dumps(js)


print(jsonobj)
