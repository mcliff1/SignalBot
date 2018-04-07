#!/usr/bin/python
#  python simulator code

# curl -X POST https://5565netqr0.execute-api.us-west-2.amazoneaws.com/dev/api/metrics/soil -d '{ "beg" : "beg " }'

import json
import os
import psycopg2
import numpy as np
import time
import urllib2


TARGET_URL_SOIL = "https://5565netqr0.execute-api.us-west-2.amazonaws.com/dev/api/metrics/soil"

class SimBot:

    def __init__(self, deviceid, 
                 volts=5.0, battery=100.00):
        self.deviceid = deviceid
        self.volts = volts
        self.battery = battery


class SoilBot():

    def __init__(self, deviceid, tempf=80,
                 soilmoisture1=3000, soilmoisture2=3000, soilmoisture3=1, 
                 humidity=20.0, volts=5.0, battery=100.00):
        self.deviceid = deviceid
        self.volts = volts
        self.battery = battery
        self.tempf = tempf
        self.tempc = (tempf-32)/1.8
        self.soilmoisture1 = soilmoisture1
        self.soilmoisture2 = soilmoisture2
        self.soilmoisture3 = soilmoisture3
        self.humidity = humidity

    def update(self, ratio=1):
        self.tempf += np.random.normal(0,0.1 * ratio)
        self.soilmoisture1 += np.random.normal(0,5 * ratio)
        self.soilmoisture2 += np.random.normal(0,5 * ratio)
        #self.soilmoisture3 += np.random.normal(0,5 * ratio)
        self.humidity += np.random.normal(0,0.1 * ratio)
        self.volts += np.random.normal(0,0.01 * ratio)
        self.battery += np.random.normal(0,0.5 * ratio)

    def status(self):
        return { "beg" : "beg",
                 "deviceid" : self.deviceid,
                 "soilmoisture1" : self.soilmoisture1,
                 "soilmoisture2" : self.soilmoisture2,
                 "soilmoisture3" : self.soilmoisture3,
                 "humidity" : self.humidity,
                 "tempc" : (self.tempf-32)/(1.8),
                 "tempf" : self.tempf,
                 "volts" : self.volts,
                 "battery" : self.battery }



def postData(bot):
    """
    posts the data to the URL end point
    """
    data = bot.status()
    req = urllib2.Request(TARGET_URL_SOIL)
    req.add_header('Content-Type', 'application/json')
    jsondata = json.dumps(data)
    jsondataasbytes = jsondata.encode('utf-8')
    req.add_header('Content-Length', len(jsondataasbytes))

    response = urllib2.urlopen(req, jsondataasbytes)
    print("send data")
    return response




# make an array of these bots
botArray = [
    SoilBot('1200aaaaffff0021'),
    SoilBot('1300aaaaffff0031'),
    SoilBot('1400aaaaffff0041'),
    SoilBot('1500aaaaffff0051', volts=3.4),
    SoilBot('1600aaaaffff0061', battery=60),
    SoilBot('1000aaaaffff0001'),
    SoilBot('2000bbaaffff0002', tempf = 90),
    SoilBot('3000ccaaffff0003', soilmoisture1=2100, soilmoisture2=2000),
    SoilBot('4000ddaaffff0004', tempf = 100)
]


while True:
    print("update and post")
    list(map(lambda x:x.update(ratio=1), botArray))
    list(map(lambda x: postData(x), botArray))
    time.sleep(5)

