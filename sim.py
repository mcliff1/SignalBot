#!/usr/bin/python
#  python simulator code

# curl -X POST https://5565netqr0.execute-api.us-west-2.amazoneaws.com/dev/api/metrics/soil -d '{ "beg" : "beg " }'


#  add some command line params

#   -n number of bots
#   
#   -v -t soil   (verbose print a single soil bot to terminal)
#
#
#



import json
import os
import psycopg2
import numpy as np
import time
import urllib2

url_endpoints = {
    'soil' : "https://5565netqr0.execute-api.us-west-2.amazonaws.com/dev/api/metrics/soil",
    'cure' : "https://5565netqr0.execute-api.us-west-2.amazonaws.com/dev/api/metrics/cure"
}

class SimBot(object):
    """
    Base Class for Simulator Bot, has temp, battery and volts embedded
    """

    def __init__(self, deviceid, bottype=None, tempf=85.0,
                 volts=5.0, battery=100.00):
        """
        base initialization
    
        for temp, we only initilize the farenheit
        """
        self.__deviceid = deviceid
        self.__bottype = bottype
        self.__volts = volts
        self.__battery = battery
        self.__tempf = tempf
        self.__tempc = (tempf-32)/1.8

    def __str__(self):
        return("%s-%s" %s (self.__bottype, self.__deviceid))

    def type(self):
        return(self.__bottype)

    def status(self):
        return { 'beg':'beg', 
                 'deviceid' : self.__deviceid,
                 'bottype' : self.__bottype,
                 'tempf' : self.__tempf,
                 'tempc' : self.__tempc,
                 'volts' : self.__volts,
                 'battery' : self.__battery }

    def update(self, ratio=1):
        self.__volts += np.random.normal(0, 0.01 * ratio) 
        self.__battery += np.random.normal(0, 0.5 * ratio) 
        self.__tempf += np.random.normal(0,0.1 * ratio)
        self.__tempc += np.random.normal(0,(0.1 * ratio)/1.8)




class CureBot(SimBot):
    """
    Cure Bot extension
    adds: infrared, uvindex, visible, humidity
    """

    def __init__(self, deviceid, 
                 infrared=250, uvindex=0.02, visible=260, 
                 humidity=20, **kwargs):
        """
        initialize the cure bot
        """
        super(CureBot, self).__init__(deviceid, bottype='cure', **kwargs)
        self.__infrared = infrared
        self.__uvindex = uvindex
        self.__visible = visible
        self.__humidity = humidity

    def update(self, ratio=1):
        super(CureBot, self).update(ratio=1)
        self.__infrared += np.random.normal(0,0.1 * ratio)
        self.__uvindex += np.random.normal(0,000.1 * ratio)
        self.__visible += np.random.normal(0,0.1 * ratio)
        self.__humidity += np.random.normal(0,0.01 * ratio)


    def status(self):
        jsondata = super(CureBot, self).status()
        jsondata['infrared'] = self.__infrared
        jsondata['uvindex'] = self.__uvindex
        jsondata['visible'] = self.__visible
        jsondata['humidity'] = self.__humidity
        return(jsondata)





class SoilBot(SimBot):
    """
    Soil Bot extension
    adds: 3 moisture, humidity, 
    """

    def __init__(self, deviceid, 
                 soilmoisture1=3000, soilmoisture2=3500, soilmoisture3=2500, 
                 humidity=20.0, **kwargs):
        """
        initialize the soil bot
        """
        super(SoilBot, self).__init__(deviceid, bottype='soil', **kwargs)
        self.__soilmoisture1 = soilmoisture1
        self.__soilmoisture2 = soilmoisture2
        self.__soilmoisture3 = soilmoisture3
        self.__humidity = humidity

    def update(self, ratio=1):
        super(SoilBot, self).update(ratio=1)
        self.__soilmoisture1 += np.random.normal(0,5 * ratio)
        self.__soilmoisture2 += np.random.normal(0,5 * ratio)
        self.__soilmoisture3 += np.random.normal(0,5 * ratio)
        self.__humidity += np.random.normal(0,0.01 * ratio)


    def status(self):
        jsondata = super(SoilBot, self).status()
        jsondata['soilmoisture1'] = self.__soilmoisture1
        jsondata['soilmoisture2'] = self.__soilmoisture2
        jsondata['soilmoisture3'] = self.__soilmoisture3
        jsondata['humidity'] = self.__humidity
        return(jsondata)




def postData(bot):
    """
    posts the data to the URL end point
    """
    data = bot.status()
    target_url = url_endpoints[bot.type()]
    if (bot.type() not in url_endpoints):
        print("error, unknoen bot type");

    req = urllib2.Request(target_url)
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
    SoilBot('1500aaaaffff0051', volts=3.4),
    SoilBot('1600aaaaffff0061', battery=60),
    SoilBot('2000bbaaffff0002', tempf = 90),
    SoilBot('3000ccaaffff0003', soilmoisture1=2100, soilmoisture2=2000),
    CureBot('4000ccaacccc0004', tempf = 32),
    CureBot('4100bbaacccc0014', tempf = 32),
]


sleep_time = 5
while True:
    print("update and post, sleep for %s seconds" % (sleep_time,))
    list(map(lambda x:x.update(ratio=1), botArray))
    list(map(lambda x: postData(x), botArray))
    time.sleep(sleep_time)

