
import json
import os
import sys
import numpy as np
from datetime import datetime, timedelta
import pandas as pd
from coords_manager import *
from json.decoder import JSONDecodeError

import time


import configparser
config = configparser.ConfigParser()
config.read('settings.ini')


# TODO uniezależnić od miejsca lokalizacji skryptu
GLOBAL_PATH = os.path.join(os.getcwd())
"""
imgw parameters - it is exatly number of column from special file
"""
# IMGW codes
# 29	air temperature
# 77	ground temperature 5 m
# 79	ground temperature 10 m
# 81	ground temperature 20 m
# 87	min_12h
# 89	max_12h
# 91    min_ground_12h
# 37	relative humidity
code_imgw_air_temp = 29
code_imgw_ground_temp_5 = 77
code_imgw_ground_temp_10 = 79
code_imgw_ground_temp_20 = 81
min_12h = 87
max_12h = 89
min_ground_12h = 91
code_imgw_rel_hum = 37

"""
list of cities for particular visualisation - this is a of list of synoptic imgw stations - polish notation
"""
# malgosia_list = ["KOŁOBRZEG-DŹWIRZYNO",  "ŁEBA", "LĘBORK", "GDAŃSK", "ELBLĄG", "KĘTRZYN",\
#                 "SUWAŁKI", "TORUŃ", "CZĘSTOCHOWA", "KATOWICE", "KRAKÓW", "SANDOMIERZ",\
#                 "BIELSKO-BIAŁA", "ZAMOŚĆ", "ZAKOPANE", "KASPROWY WIERCH"]

"""
list of cities for particular visualisation - this is a of list of synoptic imgw stations - simplified notation
"""
malgosia_list = ["KOLOBRZEG", "KOLOBRZEG-DZWIRZYNO",  "LEBA", "LEBORK", "GDANSK-SWIBNO", "ELBLAG", "KETRZYN",
                 "SUWALKI", "TORUN", "CZESTOCHOWA", "KATOWICE", "KRAKOW", "SANDOMIERZ",
                 "BIELSKO-BIALA", "JELENIA GORA", "KASPROWY WIERCH", "SWINOUJSCIE", "SNIEZKA"]


'''
from stacje_meteorologiczne.csv
load meteorologic stations. return as dataframe
'''


# ////////////////////////////////////////////////////////////////////////////////////////////////////////


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

# ////////////////////////////////////////////////////////////////////////////////////////////////////////


def load_imgw_coordinates_station():
    """
    load coordinates of stations from stacje_meteorologiczne.csv
    :param filter: filter set of imgw stations
    :param labels: Return labels - names of cities or not.
    :return: DataFrame
    """
    path = GLOBAL_PATH+"/dane_imgw/stacje_meteorologiczne.csv"
    dataframe = pd.read_csv(path, encoding='utf-8',
                            low_memory=False, header=None)

    dataframe[0] = dataframe[0].astype(str)
    dataframe[3] = dataframe[3].astype(float)/10000
    dataframe[2] = dataframe[2].astype(float)/10000
    return dataframe


def load_imgw_coordinates_station_PL():
    """
    load coordinates of stations from stacje_meteorologiczne.csv
    :param filter: filter set of imgw stations
    :param labels: Return labels - names of cities or not.
    :return: DataFrame
    """
    path = GLOBAL_PATH+"/dane_imgw/pl_stacje.csv"
    dataframe = pd.read_csv(path, encoding='utf-8',
                            low_memory=False, delimiter=';')

    # dataframe[0] = dataframe[0].astype(str)
    # dataframe[1] = dataframe[1].astype(str)
    # dataframe[2] = dataframe[2].astype(float)
    # dataframe[3] = dataframe[3].astype(float)
    # dataframe[4] = dataframe[4].astype(float)
    return dataframe


def filter_namefiles(namefiles, station):
    if station == 'all':
        return namefiles
    else:
        returned = []
        for namefile in namefiles:
            if namefile.find(station):
                return [namefile]
        return namefiles


def loadImgwCodesStations():
    values = []
    stations = load_imgw_coordinates_station_PL()
    print("shape is", stations.shape)
    for i in range(stations.shape[0]):
        values.append(int(stations.loc[i, "wmoid"]))
    return values


def loadImgwNamestations():
    names = []
    stations = load_imgw_coordinates_station_PL()
    print("shape is", stations.shape)
    for i in range(stations.shape[0]):
        rowcols.append(int(stations.loc[i, "stname"]))
    return rowcols


def load_imgw_data(year, month, day, hour, parameter, stations):

    path = GLOBAL_PATH+"/dane_imgw/"+str(year)
    namefiles = os.listdir(path)

    namefiles = filter_namefiles(namefiles, stations)
    namefiles.sort()

    direct_paths = [os.path.join(path, namefile) for namefile in namefiles]

    big_frame = pd.DataFrame()
    for f, namefile in zip(direct_paths, namefiles):
        dataframe = pd.read_csv(f, encoding='latin',
                                low_memory=False, header=None)
        dataframe_f = dataframe[(dataframe[2] == year) & (
            dataframe[3] == month) & (dataframe[4] == day) & (dataframe[5] == hour)]
        big_frame = big_frame.append(dataframe_f)

    big_frame[0] = big_frame[0].astype(str)
    cut_big_frame = big_frame[[0, parameter]]

    coordinates_array = load_imgw_coordinates_station()
    result = cut_big_frame.set_index(0).join(
        coordinates_array.set_index(0), lsuffix='_caller', rsuffix='_other')

    lat = np.array(result[2].values.tolist())
    lon = np.array(result[3].values.tolist())

    val = np.array(result[parameter].values.tolist())
    return lat, lon, val


def loadImgwRowcolNodes():
    values = []
    stations = load_imgw_coordinates_station_PL()
    print("shape is", stations.shape)
    for i in range(stations.shape[0]):
        # print("name is ", stations.loc[i, "stname"])
        # print("latlon is ", (stations.loc[i, "lat"], stations.loc[i, "lon"]))
        # print("lon is ", stations.loc[i, "lon"])
        # print("TYPE lon is ", type(stations.loc[i, "lon"]))
        lon = float(stations.loc[i, "lon"])
        lat = float(stations.loc[i, "lat"])
        rowcol = um_latlon2rowcol((lon, lat))
        values.append(rowcol)
        print("name:", stations.loc[i, "stname"], "latlon:", (
            stations.loc[i, "lat"], stations.loc[i, "lon"]), "rowcol:", rowcol)
    return values


def load_faster_imgw_data(years, parameter, stations):

    big_frame = pd.DataFrame()
    for year in years:
        path = GLOBAL_PATH+"/dane_imgw/"+str(year)
        namefiles = os.listdir(path)
        namefiles = filter_namefiles(namefiles, stations)
        namefiles.sort()
        direct_paths = [os.path.join(path, namefile) for namefile in namefiles]
        for f, in zip(direct_paths):
            dataframe = pd.read_csv(
                f, encoding='latin', low_memory=False, header=None)
            big_frame = big_frame.append(dataframe[[0, 2, 3, 4, 5, parameter]])

    return big_frame


def extract_latlonval(df, coords, year, month, day, hour, param):
    df = df[(df[2] == year) & (df[3] == month)
            & (df[4] == day) & (df[5] == hour)]
    df.loc[:, 0] = df.loc[:, 0].astype(str)
    coords[0] = coords[0].astype(str)
    result = df.set_index(0).join(coords.set_index(
        0), lsuffix='_caller', rsuffix='_other')

    lat = np.array(result["2_other"].values.tolist())
    lon = np.array(result["3_other"].values.tolist())

    val = np.array(result[param].values.tolist())
    return lat, lon, val


def load_altitude_onestation():
    path = os.path.join(GLOBAL_PATH, "dane_imgw", "pl_stacje.csv")
    dataframe = pd.read_csv(path, encoding='utf-8',
                            low_memory=False, header=None)
    dataframe[4] = dataframe[4].astype(float)
    return dataframe[4].values.tolist()


def load_imgw_pl_stations(filter=False):
    path = GLOBAL_PATH+'/dane_imgw/pl_stacje.csv'
    dataframe = pd.read_csv(path, encoding='utf-8',
                            low_memory=False, delimiter=";")
    if filter is True:
        dataframe = dataframe[np.isin(dataframe['stname'], malgosia_list)]

    return dataframe['lon'], dataframe['lat'], dataframe['stname']


'''
load a sequence map of imgw data in rowcol Poland representation
'''


def load_sequence_map(start, param=code_imgw_air_temp, forecast_hour_len=48):
    from numpy import savetxt
    spacetime = np.full(
        (forecast_hour_len, coords_manager.Poland.xlen, coords_manager.Poland.ylen), 0.0)
    for it in range(forecast_hour_len):
        n = start+timedelta(hours=it)
        try:
            spacetime[it] = load_imgw_single(
                n.year, n.month, n.day, n.hour, param=param)
            savetxt(os.path.join(os.getcwd(), '..', 'imgw_proceed_data', 'imgw_csvs', '{}-{}'.format(n.year, n.month),
                                 str(it)), spacetime[it], delimiter=",")
        except BaseException:
            pass

    return spacetime


'''
load a series for concrete localisation in rowcol Poland way
'''


def get_one_series(spacetime, rowcol):
    return spacetime[:, rowcol[0], rowcol[1]].flatten()


'''
make a map of weather parameter in a based of a IMGW synoptic stations
'''


def load_imgw_single(YEAR, MONTH, DAY, HOUR, stations='all', param=code_imgw_air_temp):
    lat_imgw, lon_imgw, nointerpolated_value_imgw = load_imgw_data(
        YEAR, MONTH, DAY, HOUR, param, stations)
    row_imgw, col_imgw = latlon2rowcol(lat_imgw, lon_imgw)
    from scipy.interpolate import Rbf
    rbf = Rbf(row_imgw, col_imgw, nointerpolated_value_imgw, epsilon=0.02)
    tiy = np.linspace(Poland.xmin, Poland.xmax, Poland.xlen)
    tix = np.linspace(Poland.ymin, Poland.ymax, Poland.ylen)
    # w meshgrid wyrażam w reprezentacji rowcol Globalnej
    YI, XI = np.meshgrid(tix, tiy)
    interpolated_value_imgw = rbf(XI, YI)
    return np.array(interpolated_value_imgw)

    # node - reprezentacja rowcol Globalnej


def load_imgw_single_point(YEAR, MONTH, DAY, HOUR, node, stations='all', param=code_imgw_air_temp):
    lat_imgw, lon_imgw, nointerpolated_value_imgw = load_imgw_data(
        YEAR, MONTH, DAY, HOUR, param, stations)
    row_imgw, col_imgw = latlon2rowcol(lat_imgw, lon_imgw)
    from scipy.interpolate import Rbf
    rbf = Rbf(row_imgw, col_imgw, nointerpolated_value_imgw, epsilon=0.02)
    # w meshgrid wyrażam w reprezentacji rowcol Globalnej
    interpolated_value_imgw = rbf(node[1], node[0])
    return round(float(interpolated_value_imgw), 2)


def mongoLoadImgwStationsSeries(start, i, station, len, param=code_imgw_air_temp):
    import pymongo
    import traceback

    startTime = time.process_time()

    currDate = start
    stations = load_imgw_coordinates_station_PL()
    accuracy = 4

    short_code = stations.loc[i, "wmoid"]
    name = stations.loc[i, "stname"]
    lat = round(float(stations.loc[i, "lat"]), accuracy)
    lon = round(float(stations.loc[i, "lon"]), accuracy)
    rowcol = um_latlon2rowcol((lon, lat))
    row = int(rowcol[0])
    col = int(rowcol[1])
    node_latlon = um_rowcol2latlon((row, col))
    node_lat = round(node_latlon[0], accuracy)
    node_lon = round(node_latlon[1], accuracy)

    print("name:", name, "latlon:", (lat, lon), "rowcol", (rowcol))

    database = pymongo.MongoClient(config["DEFAULT"]["database"])
    mydb = database[config['DEFAULT']['collectionname']]
    myColl = mydb["IMGWraw"]

    currYear = 0
    for currDate in [start+timedelta(hours=it) for it in range(len)]:
        if currYear < currDate.year:
            df = load_faster_imgw_data(
                [currDate.year], param, str(short_code)[2:])
            print("data loaded for year {}", currDate.year)
            currYear = currDate.year
        m = currDate.month
        d = currDate.day
        h = currDate.hour
        condition = (df[3] == m) & (df[4] == d) & (df[5] == h)
        rowDataframe = df[condition]
        if not rowDataframe.empty:
            dfvalue = rowDataframe[[param]]
            print("current date is:", currDate)
            # print(rowDataframe)
            value = float(dfvalue.values.tolist()[0][0])
            print("value is ", value)
            #print("typevalue is ", type(value))
            myColl.insert_one({"short_code": str(short_code), "name": str(name), "date_imgw": currDate, "param": param, "value_imgw": value,
                               "lat": lat, "lon": lon, "node_lat": node_lat, "node_lon": node_lon, "row": row, "col": col})

    endTime = time.process_time()

    print("performance for station {}, {} hours is {} seconds".format(
        station, len, (endTime-startTime)))


def mongo_load_imgw_series(d, node, stations='all', param=code_imgw_air_temp, len=30):
    from scipy.interpolate import Rbf
    import pymongo
    import traceback

    start = d
    coords = load_imgw_coordinates_station()
    first = d.year
    last = (start+timedelta(hours=len)).year
    years = list(range(first, last+1))
    df = load_faster_imgw_data(years, param, stations)

    start_timer = time.process_time()

    database = pymongo.MongoClient(config["DEFAULT"]["database"])
    mydb = database[config['DEFAULT']['collectionname']]
    mycoll = mydb["IMGW"]

    for d in [start+timedelta(hours=it) for it in range(len)]:
        #print("d {}".format(d))
        lat_imgw, lon_imgw, nointerpolated_value_imgw = extract_latlonval(
            df, coords, d.year, d.month, d.day, d.hour, param)
        row_imgw, col_imgw = latlon2rowcol(lat_imgw, lon_imgw)
        try:
            rbf = Rbf(row_imgw, col_imgw,
                      nointerpolated_value_imgw, epsilon=0.02)
            # TODO upewnić się czy kolejność jest dobra tutaj
            value = np.round(rbf(node[1], node[0]), 3)
            # print(d)

            mycoll.insert_one({"date_imgw": d, "stations": stations,
                               "row": int(node[0]), "col": int(node[1]), "param": param, "value_imgw": value})
        except Exception:
            pass
            #print("error - matrix is singular for ", d)
            # traceback.print_exc()

    end_timer = time.process_time()
    print("performance time for {} is {}".format(node, (end_timer-start_timer)))


def mongo_load_um_series(start, node, number_forecasts):

    # a - anticipation
    import json
    import pymongo

    def k2c(t):
        return t-273.15

    def c2k(t):
        return t+273.15

    start_timer = time.process_time()

    print("config!!!!!", config['DEFAULT']['database'])
    database = pymongo.MongoClient(config['DEFAULT']['database'])
    mydb = database[config['DEFAULT']['collectionname']]
    mycoll = mydb["UM"]

    um_series = []
    for i in range(number_forecasts):

        d = start + timedelta(days=i)
        print("check if date is in utc time: ", d)
        YEAR, MONTH, DAY, HOUR = d.year, d.month, d.day, d.hour

        # TODO uniezależnić to miejsce od miejsca uruchamiania skryptu

        if not os.path.isdir("um_data/{}_{}".format(node[0], node[1])):
            os.mkdir("um_data/{}_{}".format(node[0], node[1]))

        grid = get_grid(d, "03236_0000000")
        print("{} for date {} and node {}".format(grid, d, node))
        command = "curl https://api.meteo.pl/api/v1/model/um/grid/{}/coordinates/{},{}/field/03236_0000000/level/_/date/{}-{}-{}T{}/forecast/ -X POST -H 'Authorization: Token 35f9b4a3ae7a274c1b12a8e3020ce69b180661ea' > um_data/{}_{}/{}-{}-{}T{}.txt"
        command_final = command.format(
            grid, node[0], node[1], YEAR, MONTH, DAY, HOUR, node[0], node[1], YEAR, MONTH, DAY, HOUR)
        os.popen(command_final)
        time.sleep(0.8)

        path = "um_data/{}_{}/{}-{}-{}T{}.txt".format(
            node[0], node[1], YEAR, MONTH, DAY, HOUR)
        #print("iteration number is {} path is: {} ".format(i, path))
        f = open(path, 'r')

        try:
            forecast = json.loads(f.read())
        except JSONDecodeError as e:
            print(e, " ERROR, json has not required format or file is incorrect")

        try:
            values = [round(k2c(i), 3) for i in forecast['data'][::4]]
            for i, value in enumerate(values):

                dbrow = {"start_forecast": d, "date_um": d +
                         timedelta(hours=i), "row": int(node[0]), "col": int(node[1]), "value_um": value, "grid": grid}
                mycoll.insert_one(dbrow)
                print("start_forecast", d, "date", d +
                      timedelta(hours=i), "value=", value)
        except TypeError as e:
            print("for {d} we don't have forecast".format(d=d))

    end_timer = time.process_time()
    print("performance time is {}".format(end_timer-start_timer))
