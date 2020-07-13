import time
import os
from datetime import datetime, timedelta, timezone
from json import *
import sys
import json


def readInfo():
    infoPath = 'info_dict.json'
    with open(infoPath, 'r') as f:
        info = json.load(f)
        return info


def to_datetime(date: str):
    return datetime.strptime(date, '%Y-%m-%dT%H%z')


def get_grid(day, field):
    info = readInfo()
    info = info[field]
    for i in info:
        if to_datetime(i['start_date']) <= day <= to_datetime(i['end_date']):
            return i['info']['grid']


# PARAMS ###
# (ROW, COL)
# (264, 280) - okolice suwałk
# (175, 162) - kotlina jeleniogórska - łysa góra
NODES = [
    # (264, 280),  # okolice suwałk
    # (175, 162),  # kotlina jeleniogórska - łysa góra
    # (281, 195),  # łeba forest
    # (281, 196),  # łeba urban
    # (255, 268)   # jeziora
    (211, 233)
]

for node in NODES:
    length = 365*5+150
    YEAR, MONTH, DAY, HOUR = 2015, 1, 1, 0
    start = datetime(YEAR, MONTH, DAY, HOUR, tzinfo=timezone.utc)
    os.mkdir("../um_data/{}_{}".format(node[0], node[1]))
    for i in range(length):
        time.sleep(0.6)
        d = start + timedelta(days=i)
        YEAR, MONTH, DAY, HOUR = d.year, d.month, d.day, d.hour
        grid = get_grid(d, "03236_0000000")
        print("{} for date {} and node {}".format(grid, d, node))
        command = "curl https://api.meteo.pl/api/v1/model/um/grid/{}/coordinates/{},{}/field/03236_0000000/level/_/date/{}-{}-{}T{}/forecast/ -X POST -H 'Authorization: Token 35f9b4a3ae7a274c1b12a8e3020ce69b180661ea' > ../um_data/{}_{}/{}-{}-{}T{}.txt"
        command_final = command.format(
            grid, node[0], node[1], YEAR, MONTH, DAY, HOUR, node[0], node[1], YEAR, MONTH, DAY, HOUR)
        os.popen(command_final)
