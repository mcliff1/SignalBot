#!/usr/bin/python
#  python simulator code

# curl -X POST https://5565netqr0.execute-api.us-west-2.amazoneaws.com/dev/api/metrics/soil -d '{ "beg" : "beg " }'

import json
import os
import psycopg2
import numpy as np


class SimBotClass:

    def __init__(self, deviceid, tempf=80,
                 soilmoisture1=3000, soilmoisture2=3000, soilmoisture3=1, 
                 humidity=20.0, volts=5.0, battery=100.00):
        self.deviceid = deviceid
        self.tempf = tempf
        self.soilmoisture1 = soilmoisture1
        self.soilmoisture2 = soilmoisture2
        self.soilmoisture3 = soilmoisture3
        self.humidity = humidity
        self.volts = volts
        self.battery = battery

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
                 "batterty" : self.battery }



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
print(simulateRecord())
print("goodbye world")

x = SimBotClass('testid0001')
print(x.status())
