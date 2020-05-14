

# PARAMS ###
node = (264, 280)
YEAR, MONTH, DAY, HOUR = 2016, 1, 1, 0
length = 365

import os, time
from json import *
from datetime import datetime, timedelta
start = datetime(YEAR, MONTH, DAY, HOUR)
for i in range(length):
    print("Printed immediately.")
    time.sleep(0.6)
    print("Printed after 0.6 seconds.")
    d = start + timedelta(days=i)
    YEAR, MONTH, DAY, HOUR = d.year, d.month, d.day, d.hour
    print(d)
    com = "curl https://api.meteo.pl/api/v1/model/um/grid/C5/coordinates/{},{}/field/03236_0000000/level/_/date/{}-{}-{}T{}/forecast/ -X POST -H 'Authorization: Token 35f9b4a3ae7a274c1b12a8e3020ce69b180661ea' > um_data/{}-{}-{}T{}.txt ".format(node[0], node[1], YEAR, MONTH, DAY, HOUR, YEAR, MONTH, DAY, HOUR)
    os.popen(com)


