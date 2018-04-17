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


from simbot.simbot import CureBot
from simbot.simbot import AquaBot
from simbot.simbot import LightBot
from simbot.simbot import SoilBot
from simbot.simbot import GasBot



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
