#!/usr/bin/python
#  python simulator code

import json
import os
import psycopg2
import numpy as np

rds_host = os.environ['RDS_HOST']
rds_name = os.environ['RDS_DBNAME']
rds_username = os.environ['RDS_USERNAME']
rds_password = os.environ['RDS_PASSWORD']


conn = None

def openConnection():
    global conn
    try:
        if (conn is None):
            conn = psycopg2.connect(dbname = rds_name, host = rds_host, user = rds_username, password = rds_password)
        elif (not conn.open):
            conn = psycopg2.connect(dbname = rds_name, host = rds_host, user = rds_username, password = rds_password)
    except Exception as e:
        print(e)
        raise e



def simulateRecord():
    tempf = 90 + np.random.normal(0,5)
   
    s = [{ "beg":"beg" }]
    s[0]['deviceid'] = "0001ffffffff0001"
    s[0]['soilmoisture1'] = 3300 + np.random.normal(0,50)
    s[0]['soilmoisture2'] = 3500 + np.random.normal(0,50)
    s[0]['soilmoisture3'] = 1
    s[0]['humidity'] = 1
    s[0]['tempc'] = 100 * (tempf - 32)/(212 - 32)
    s[0]['volts'] = 4.2 + np.random.normal(0,.1)
    s[0]['battery'] = 104 + np.random.normal(0,6)

    return s

    

print("hello world")
openConnection()
print(simulateRecord())
print("goodbye world")
