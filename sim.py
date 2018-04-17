#!/usr/bin/python
"""
  python Signal simulator code
  author: Matt Cliff
  created: April 7, 2018


  TODO: add some command line params
   -n number of bots

   -v -t soil   (verbose print a single soil bot to terminal)
"""

import json
import time
import urllib2
import argparse
import numpy as np

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
        return("%s-%s" % (self.__bottype, self.__deviceid))

    def type(self):
        """
        identifies the type of bot instance
        """
        return(self.__bottype)

    def status(self):
        """
        returns a JSON string describing itself
        """
        return {
            'beg':'beg',
            'deviceid' : self.__deviceid,
            'bottype' : self.__bottype,
            'tempf' : self.__tempf,
            'tempc' : self.__tempc,
            'volts' : self.__volts,
            'battery' : self.__battery
        }

    def update(self, ratio=1):
        """
        runs one time unit on the simulation to update with some noise
        """
        self.__volts += np.random.normal(0, 0.01 * ratio)
        self.__battery += np.random.normal(0, 0.5 * ratio)
        if self.__battery > 105:
            self.__battery -= 1.5
        self.__tempf += np.random.normal(0, 0.1 * ratio)
        self.__tempc += np.random.normal(0, (0.1 * ratio)/1.8)




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
        self.__infrared += np.random.normal(0, 0.1 * ratio)
        self.__uvindex += np.random.normal(0, 000.1 * ratio)
        self.__visible += np.random.normal(0, 0.1 * ratio)
        self.__humidity += np.random.normal(0, 0.01 * ratio)


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
        self.__soilmoisture1 += np.random.normal(0, 5 * ratio)
        self.__soilmoisture2 += np.random.normal(0, 5 * ratio)
        self.__soilmoisture3 += np.random.normal(0, 5 * ratio)
        self.__humidity += np.random.normal(0, 0.01 * ratio)


    def status(self):
        jsondata = super(SoilBot, self).status()
        jsondata['soilmoisture1'] = self.__soilmoisture1
        jsondata['soilmoisture2'] = self.__soilmoisture2
        jsondata['soilmoisture3'] = self.__soilmoisture3
        jsondata['humidity'] = self.__humidity
        return(jsondata)







class AquaBot(SimBot):
    """
    Aqua Bot extension
    adds: ec, sal, sg, tds, ph, doxygen
    """

    def __init__(self, deviceid,
                 ec=4.45, sal=0, sg=1, tds=3, ph=7,
                 doxygen=2.8, **kwargs):
        """
        initialize the aqua bot
        """
        super(AquaBot, self).__init__(deviceid, bottype='aqua', **kwargs)
        self.__ec = ec
        self.__sal = sal
        self.__sg = sg
        self.__tds = tds
        self.__ph = ph
        self.__doxygen = doxygen

    def update(self, ratio=1):
        super(AquaBot, self).update(ratio=1)
        self.__ec += np.random.normal(0, 0.01 * ratio)
        self.__sal += np.random.normal(0, 0.001 * ratio)
        if self.__sal < 0:
            self.__sal = 0.01
        self.__sg += np.random.normal(0, 0.001 * ratio)
        self.__tds += np.random.normal(0, 0.01 * ratio)
        self.__ph += np.random.normal(0, 0.01 * ratio)
        self.__doxygen += np.random.normal(0, 0.01 * ratio)


    def status(self):
        jsondata = super(AquaBot, self).status()
        jsondata['ec'] = self.__ec
        jsondata['sal'] = self.__sal
        jsondata['sg'] = self.__sg
        jsondata['tds'] = self.__tds
        jsondata['ph'] = self.__ph
        jsondata['doxygen'] = self.__doxygen
        return(jsondata)








class LightBot(SimBot):
    """
    Light Bot extension
    adds: lux, par, infrared, fullspec, visible, humidity
    """

    def __init__(self, deviceid,
                 lux=25, par=0.45, fullspec=280, visible=260,
                 infrared=180, humidity=20, **kwargs):
        """
        initialize the cure bot
        """
        super(LightBot, self).__init__(deviceid, bottype='light', **kwargs)
        self.__lux = lux
        self.__par = par
        self.__fullspec = fullspec
        self.__visible = visible
        self.__infrared = infrared
        self.__humidity = humidity

    def update(self, ratio=1):
        super(LightBot, self).update(ratio=1)
        self.__infrared += np.random.normal(0, 0.1 * ratio)
        # dont change par or lux
        self.__fullspec += np.random.normal(0, 0.1 * ratio)
        self.__visible += np.random.normal(0, 0.1 * ratio)
        self.__humidity += np.random.normal(0, 0.01 * ratio)


    def status(self):
        jsondata = super(LightBot, self).status()
        jsondata['par'] = self.__par
        jsondata['lux'] = self.__lux
        jsondata['infrared'] = self.__infrared
        jsondata['fullspec'] = self.__fullspec
        jsondata['visible'] = self.__visible
        jsondata['humidity'] = self.__humidity
        return(jsondata)








class GasBot(SimBot):
    """
    Gas Bot extension
    adds: carbondioxide
    """

    def __init__(self, deviceid,
                 carbondioxide=80,
                 **kwargs):
        """
        initialize the gas bot
        """
        super(GasBot, self).__init__(deviceid, bottype='gas', **kwargs)
        self.__carbondioxide = carbondioxide

    def update(self, ratio=1):
        super(GasBot, self).update(ratio=1)
        self.__carbondioxide += np.random.normal(0, 0.1 * ratio)


    def status(self):
        jsondata = super(GasBot, self).status()
        jsondata['carbondioxide'] = self.__carbondioxide
        return(jsondata)



#----------------------end section for class defition



def post_data(bot, url):
    """
    posts the status data to the URL end point:  url+bot.type()
    """
    data = bot.status()
    #response = None
    #if (bot.type() in url_endpoints):
    target_url = url + bot.type()
    req = urllib2.Request(target_url)
    req.add_header('Content-Type', 'application/json')
    jsondata = json.dumps(data)
    jsondataasbytes = jsondata.encode('utf-8')
    req.add_header('Content-Length', len(jsondataasbytes))

    response = urllib2.urlopen(req, jsondataasbytes)
    print("send %s rc:%s" % (bot, response.code))
    return response



def main(bot_list, url):
    """
    Continuous loop to post all bots to the URL
    """


    parser = argparse.ArgumentParser(prog='sim', description='simulates Signal Bots generating and posting JSON data')
    parser.add_argument('-f', '--foo', help='foo help')
    parser.add_argument('-s', '--sleep', type=int, nargs='?', default=5, help='sleep time in seconds (default 5)')
    parser.add_argument('-d', '--dump', help='dump a single record to stdout')
    parser.add_argument('-u', '--url', help='URL to post to (does not include {bottype}', default=url)
    args = vars(parser.parse_args())

    sleep_time = args['sleep']
    dump_type = args['dump']
    url = args['url']  #  pull through the arg tool if updated
 
    if dump_type is not None:
        print("I really need to do something here with %s" % dump_type)
        # exit the main method without going into the loop
        bot = SoilBot("dummy000aaabbb")
        print(bot.status())
        return

 
    print("POSTING to url %s%s" % (url, '{bottype}'))
    while True:
        print("update and post, sleep for %s seconds" % (sleep_time,))
        list(map(lambda x: x.update(ratio=1), bot_list))
        list(map(lambda x: post_data(x, url), BOT_ARRAY))
        #list(map(post_data, bot_list))
        time.sleep(sleep_time)


if __name__ == '__main__':
    """  run this if we are called as the primary module
    """

    # make an array of these bots
    BOT_ARRAY = [
        SoilBot('1200aaaaffff0021'),
        SoilBot('1300aaaaffff0031'),
        SoilBot('1500aaaaffff0051', volts=3.4),
        SoilBot('1600aaaaffff0061', battery=60),
        SoilBot('2000bbaaffff0002', tempf=90),
        SoilBot('3000ccaaffff0003', soilmoisture1=2100, soilmoisture2=2000),
        CureBot('4000ccaacccc0004', tempf=32),
        AquaBot('5000ccaaaaaa0005'),
        AquaBot('5100bbaaaaaa0015'),
        LightBot('6000bbaa11110006'),
        LightBot('6100bbaa11110016'),
        LightBot('6200bbaa11110026'),
        GasBot('7000bbaagggg0007'),
    ]

    url_rds = "https://i0959l88u2.execute-api.us-west-2.amazonaws.com/dev/api/metrics/"
    url_ddb = "https://6chpacjxci.execute-api.us-west-2.amazonaws.com/dev/api/metrics/"
    main(bot_list=BOT_ARRAY, url=url_ddb)
