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


from signalbot import CureBot
from signalbot import AquaBot
from signalbot import LightBot
from signalbot import SoilBot
from signalbot import GasBot

from signalbot import Config



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



def main(bot_list):
    """
    Continuous loop to post all bots to the URL
    """

    #parser.add_argument('-s', '--save', action="store_true", help='saves URL to NAME in config')
    #parser.add_argument('-r', '--remove', action="store_true", help='removes NAME from the config')
    #parser.add_argument('-a', '--action', help='HTTP action - post get put delete')
    #parser.add_argument('-u', '--url', help='URL to post to (overrides NAME)')
    #parser.add_argument('-d', '--data', help='JSON formatted string to pass in')
    #parser.add_argument('-v', '--verbose', action="store_true", help='shows full output')
    URLS = {
       'rds' : "https://vwqqwu30m0.execute-api.us-west-2.amazonaws.com/dev/api/metrics/",
       'ddb' : "https://1ujflj28sk.execute-api.us-west-2.amazonaws.com/dev/api/metrics/"
    }


    parser = argparse.ArgumentParser(prog='sim', description='simulates Signal Bots generating and posting JSON data')
    parser.add_argument('-l', '--list', action="store_true", help='print list of saved endpoints and exit')
    parser.add_argument('-s', '--sleep', type=int, nargs='?', default=5, help='sleep time in seconds (default 5)')
    parser.add_argument('-d', '--dump', help='dump a single record to stdout')
    #parser.add_argument('-u', '--url', help='URL to post to (does not include {bottype}', default=url)
    parser.add_argument('-n', '--name', help='name to reference the ur')
    args = vars(parser.parse_args())

    sleep_time = args['sleep']
    dump_type = args['dump']

    if args['list'] is not False:
        print("list out the URL keys we have stored")
        for url in URLS:
            print('%s : %s' % (url, URLS[url]))
        return

 
    if dump_type is not None:
        print("I really need to do something here with %s" % dump_type)
        # exit the main method without going into the loop
        bot = SoilBot("dummy000aaabbb")
        print(bot.status())
        return

    if args['name'] is None:
        print('use the -n option to specify a name of an endpoint to use')
        return

    url = URLS[args['name']]
    print("POSTING to url %s%s" % (url, '{bottype}'))
    while True:
        print("update and post, sleep for %s seconds" % (sleep_time,))
        list(map(lambda x: x.update(ratio=1), bot_list))   # update the state of each bot
        list(map(lambda x: post_data(x, url), BOT_ARRAY))  # upload to back-end
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

    main(bot_list=BOT_ARRAY)


