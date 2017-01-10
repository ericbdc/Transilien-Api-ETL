from configuration import API_USER, API_PASSWORD, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB_NAME, MYSQL_HOST, MONGO_HOST, MONGO_USER, MONGO_DB_NAME, MONGO_PASSWORD
import defusedxml.ElementTree as ET

import os
import time
from datetime import datetime
import ipdb
import requests
import json
import xmltodict
import pandas as pd
# import mysql.connector
from pymongo import MongoClient


station_ids = [87113803, 87116012, 87001479, 87113852, 87116269, 87113514,
               87113894, 87116301, 87116244, 87113845, 87116517, 87116731,
               87116558, 87116368, 87116665, 87116350, 87276071, 87271510,
               87271411, 87271437, 87271247, 87276063, 87276113, 87393157,
               87386664, 87386409, 87386318, 87386425, 87393405, 87386680,
               87393363, 87393462, 87393066, 87382432, 87381715, 87382341,
               87383281, 87382374, 87381160, 87381186, 87386003, 87381194,
               87381210, 87381020, 87334482, 87276600, 87276543, 87276667,
               87276758, 87381095, 87381087, 87337980, 87381145, 87276196,
               87276519, 87276485, 87276493, 87276527, 87276535, 87276162,
               87276238, 87276188, 87276444, 87546192, 87681155, 87682138,
               87681353, 87681338, 87682179, 87546200, 87681411, 87681619,
               87682252, 87545210, 87545285, 87545178, 87545145, 87545160,
               87545475, 87393561, 87394007, 87545731, 87393488, 87682542,
               87682278, 87682427, 87683227, 87684217, 87686030, 87684241,
               87754994, 87683268, 87758060, 87686667, 87758045, 87730069,
               87758011, 87758748, 87758854, 87758763, 87116509, 87271163,
               87271304, 87116616, 87271171, 87271445, 87271015, 87116400,
               87116582, 87113795, 87113779, 87115873, 87113860, 87113886,
               87276261, 87272021, 87276139, 87271577, 87271593, 87276592,
               87276394, 87276279, 87276634, 87276360, 87281873, 87276402,
               87276410, 87393843, 87393413, 87386649, 87393009, 87382887,
               87393082, 87382440, 87393876, 87393033, 87394130, 87381905,
               87381129, 87381137, 87381798, 87382333, 87381079, 87381657,
               87381483, 87382382, 87381582, 87681635, 87681601, 87682153,
               87681452, 87682518, 87682104, 87682500, 87682120, 87682476,
               87682203, 87545459, 87545186, 87545350, 87492108, 87608802,
               87545517, 87547026, 87545129, 87543090, 87415604, 87684126,
               87684100, 87758334, 87758193, 87758086, 87683128, 87758326,
               87758110, 87758367, 87683003, 87758698, 87758672, 87758805,
               87758706, 87758599, 87113407, 87113522, 87113746, 87116020,
               87116087, 87116095, 87116111, 87116178, 87116228, 87116277,
               87116491, 87116566, 87116640, 87116749, 87116772, 87164780,
               87164798, 87271023, 87271429, 87271452, 87271460, 87271486,
               87272047, 87276055, 87276170, 87276220, 87276246, 87276253,
               87276287, 87276345, 87276550, 87276626, 87276675, 87332932,
               87332957, 87381111, 87381178, 87381228, 87381236, 87381418,
               87381459, 87381475, 87381491, 87381509, 87381558, 87381566,
               87381624, 87381848, 87381863, 87382200, 87382259, 87382267,
               87382358, 87386300, 87387092, 87391532, 87393074, 87393173,
               87393207, 87393215, 87393280, 87393306, 87393439, 87393454,
               87393512, 87393546, 87393579, 87393637, 87393652, 87430900,
               87430918, 87540179, 87545111, 87545236, 87545269, 87545293,
               87545756, 87546317, 87547315, 87681007, 87681304, 87681312,
               87681346, 87681387, 87681395, 87681478, 87681510, 87681627,
               87682005, 87682112, 87682146, 87682161, 87682294, 87682419,
               87683102, 87683136, 87683243, 87684001, 87684415, 87758003,
               87116046, 87113712, 87116038, 87113209, 87116079, 87070902,
               87116293, 87116319, 87272146, 87271528, 87271395, 87271403,
               87116103, 87116376, 87116574, 87116673, 87382481, 87381897,
               87382002, 87382218, 87382465, 87382457, 87381871, 87381830,
               87381152, 87381590, 87381806, 87381814, 87276659, 87381038,
               87332973, 87381244, 87276089, 87271148, 87276451, 87276469,
               87276501, 87276154, 87276576, 87276568, 87276436, 87276006,
               87386656, 87386730, 87393058, 87382861, 87382879, 87386573,
               87384008, 87393322, 87393421, 87393256, 87393223, 87393272,
               87393108, 87393348, 87393116, 87681825, 87545483, 87682187,
               87546291, 87681437, 87545301, 87681403, 87681379, 87545525,
               87545707, 87682443, 87682468, 87682450, 87682401, 87682302,
               87758037, 87754986, 87758318, 87758136, 87758607, 87393504,
               87393629, 87545277, 87393645, 87545137, 87393835, 87394148,
               87394114, 87419952, 87394155, 87988709, 87785436, 87758870,
               87758730, 87758771, 87758722, 87758656, 87758847, 87758664,
               87111278, 87113001, 87366922, 87381046, 87281899, 87381012,
               87328328, 87332965, 87381202, 87332940, 87276030, 87276386,
               87271122, 87276105, 87276022, 87271478, 87276642, 87276147,
               87276097, 87276584, 87113472, 87113704, 87113696, 87113217,
               87113878, 87116210, 87116137, 87116160, 87116285, 87116327,
               87271536, 87272039, 87272054, 87271031, 87271205, 87116343,
               87271551, 87116392, 87116632, 87271585, 87381426, 87381731,
               87381574, 87381822, 87381723, 87382804, 87386052, 87382499,
               87382366, 87382655, 87381889, 87382473, 87382812, 87386763,
               87393124, 87393298, 87393165, 87386417, 87393314, 87393041,
               87391565, 87391003, 87387001, 87681809, 87681247, 87545491,
               87545509, 87547307, 87681361, 87546226, 87681486, 87393884,
               87393892, 87393447, 87393611, 87393538, 87415885, 87415893,
               87430884, 87430819, 87393470, 87543207, 87545202, 87545228,
               87545194, 87543181, 87545251, 87545152, 87545467, 87545244,
               87431791, 87682526, 87684118, 87684191, 87682211, 87682435,
               87683219, 87683201, 87684407, 87758169, 87758631, 87758102,
               87758078, 87758094, 87758144, 87758151, 87758177, 87758185,
               87758201, 87758342, 87758375, 87758615, 87758623, 87758680,
               87758755, 87758839, 87758862, 87758128, 87758029, 87758052,
               87758649, 87684233, 87758359, 87758896, 87758813, 87758888,
               87988717, 87758714, 87758821]

# example_url = "http://api.transilien.com/gare/87393009/depart/"


def extract_save_station(station, api_user, api_password, collection):
    print("Extraction for station %s" % station)
    core_url = "http://api.transilien.com/"
    url = os.path.join(core_url, "gare", str(station), "depart")
    response = requests.get(url, auth=(API_USER, API_PASSWORD))
    print(response.text)
    mydict = xmltodict.parse(response.text)
    trains = mydict["passages"]["train"]
    df_trains = pd.DataFrame(trains)
    df_trains["request_date"] = datetime.now(
    ).strftime('%Y%m%dT%H%M%S')
    df_trains["station"] = station
    data_json = json.loads(df_trains.to_json(orient='records'))
    print(data_json)
    print(df_trains.to_json(orient='records'))
    collection.insert_many(data_json)

# Connect to mongodb:
c = MongoClient(host=MONGO_HOST)
db = c[MONGO_DB_NAME]
db.authenticate(MONGO_USER, MONGO_PASSWORD)
collection = db["departures"]
# db.command("collstats","departures")

# Bug d'import sur pythonanywhere
# df_gares = pd.read_csv("Data/gares_transilien.csv", sep=";")
# station_ids = df_gares["Code UIC"].values

begin_time = datetime.now()


# Programm run for an hour before new instance
while (datetime.now() - begin_time).seconds < 3600:

    loop_begin_time = datetime.now()
    # Every minute, computes half of stations, then other half
    for station in station_ids[:250]:
        try:
            extract_save_station(station, API_USER, API_PASSWORD, collection)
        except Exception as e:
            # Horrible coding, but work for now, so that a failing request does
            # not stop the whole process if no result
            print(e)
            with open("log.txt", "a") as myfile:
                myfile.write(str(station) + "\n")
            continue

    time_passed = (datetime.now() - loop_begin_time).seconds
    print(time_passed)
    if time_passed < 60:
        time.sleep(60 - time_passed)

    for station in station_ids[250:]:
        try:
            extract_save_station(station, API_USER, API_PASSWORD, collection)
        except Exception as e:
            # Horrible coding, but work for now, so that a failing request does
            # not stop the whole process if no result
            with open("log.txt", "a") as myfile:
                myfile.write(str(station) + "\n")
            continue

    # Cycles of 120 seconds for whole process
    time_passed = (datetime.now() - loop_begin_time).seconds
    print(time_passed)
    if time_passed < 120:
        time.sleep(120 - time_passed)


"""
# FOR MYSQL CLIENT

cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                              host=MYSQL_HOST,
                              database=MYSQL_DB_NAME)
cursor = cnx.cursor()

add_departure = ("INSERT INTO departures "
                 "(station, request_date, date, num, miss, term, etat) "
                 "VALUES (%s, %s, %s, %s, %s, %s, %s)")


for df in df_list:
    data_departure = {}
    cursor.execute(add_departure, data_departure)
    # emp_no = cursor.lastrowid, if we want last id created
"""
