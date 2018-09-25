#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
for python 2.7

pyapi.py <options>
  --list displays all saved urlnames (overrides all over options)
  --action GET, POST, PUT, or DELET HTTP action to call (required this or save)
  --url the URL string to send the request too (overrides urlname)
  --urlname the name to use from ~/.pyapi config file
  --save persists the provided <URL> to <URLNAME> (requires this or action)


Author: Matt Cliff
Created: 25 Apr 2018
"""
import os
import ast
import argparse
import json
import dbm
import urllib
import requests


config_file = os.path.join(os.getenv("HOME"), '.pyapi')
methods = {
    'post' : lambda url, data: requests.post(url, data=data),
    'get' : lambda url, data : requests.get(url, params=data),
    'put' : lambda url, data : requests.put(url, data=data),
    'delete' : lambda url, data : requests.delete(url, data=data),
    'options' : lambda url, data : requests.options(url, data=data)
}


def dump_config():
    """
    prints out the saved configuration
    """
    print "open db file %s for reading" % config_file
    #config_db = dbm.open(config_file, 'c')
    #config_db.close()
    #with dbm.open(config_file, 'c') as db:
    db = dbm.open(config_file, 'c')
    for key in db.keys():
        print "%s : %s" % (key.decode(), db[key].decode())
    db.close()


def get_config(name):
    """
    saves a url to the name

    """
    db = dbm.open(config_file, 'c')
    url = db[name]
    db.close()
    return url


def save_config(name, url):
    """
    saves a url to the name

    """
    db = dbm.open(config_file, 'c')
    db[name] = url
    db.close()

def remove_config(name):
    """
    removes the name from configuration

    if name isnt there throughs a KeyError
    """
    db = dbm.open(config_file, 'c')
    del db[name]
    db.close()



def main():
    """
    Utility to call/invoke API
    """


    parser = argparse.ArgumentParser(prog='pyapi', description='PYthon API caller utilty')
    parser.add_argument('-l', '--list', action="store_true", help='print list of saved names and exit')
    parser.add_argument('-s', '--save', action="store_true", help='saves URL to NAME in config')
    parser.add_argument('-r', '--remove', action="store_true", help='removes NAME from the config')
    parser.add_argument('-a', '--action', help='HTTP action - post get put delete')
    parser.add_argument('-n', '--name', help='name to reference the url in ~/.pyapi')
    parser.add_argument('-u', '--url', help='URL to post to (overrides NAME)')
    parser.add_argument('-d', '--data', help='JSON formatted string to pass in')
    parser.add_argument('-v', '--verbose', action="store_true", help='shows full output')
    args = vars(parser.parse_args())

    #print args
    #exit()


    if args['list'] is not False:
        dump_config()
        return(0)

    if args['remove'] is not False:
        if args['name'] is None:
            print "--name must be present with the --remove option"
            return(-6)
        remove_config(args['name'])
        return(0)

    action = args['action']
    if action is not None and action not in methods.keys():
        print "unknown action '%s'" % action
        return(-3)

    if args['url'] is None and args['name'] is None:
        print "you must include either a url or name"
        return(-2)

    if action is None and args['save'] is False:
        print "you must include either a action or save"
        return(-5)

    if action is not None:
        # execute the action now
        target = args['url'] if args['url'] is not None else get_config(args['name'])
        data = None if args['data'] is None else ast.literal_eval(args['data'])
        response = methods[action](target, data)

        if args['verbose'] is not False:
            print response.text
        print response.status_code


    if args['save'] is not False:
        if args['url'] is None or args['name'] is None:
            print "both --url and --name must be present with the --save option"
            return(-4)
        save_config(args['name'], args['url'])

if __name__ == "__main__":
    main()
