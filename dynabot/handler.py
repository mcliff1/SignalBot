"""
handler.py

author: matt cliff
created: april 8, 2018

AWS lambda python 3.6 code
provides RESTful endpoint to /api/metrics/{bottype}
for: soil, cure, aqua, gas, and light bots

Modification from bot;  this is to backend to DynamoDB which we will control in this unit
re: https://github.com/serverless/examples/blob/master/aws-python-rest-api-with-dynamodb/
  
"""
import os
import datetime
import json
import logging
from decimal import Decimal


import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
db_table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


def decode_json(dct):
    """
    wraps float with Decimal and general serialization to insert into dyanamo
    """
    for key, val in dct.items():
        logging.info("1{%s, %s} type - %s", key, val, type(val))
        if isinstance(val, float):
            logging.info("setting %s to Decimal", key)
            dct[key] = Decimal(str(val))
            logging.info("type is %s", type(dct[key]))
        else:
            try:
                dct[key] = TypeSerializer().serialize(val)
            except:
                dct[key] = val


    # loop throught a second time
    for key, val in dct.items():
        logging.info("2{%s, %s} type - %s", key, val, type(val))

    return dct



# these are all we support
BOT_TYPES = [ 'soil', 'cure', 'aqua', 'gas', 'light' ]




def post_call(bot_type, in_json):
    """
    generic function inserts keys from the json string

    TODO checks
    - ensure bottype in payload matches from URI
    - ensure deviceid exists
    - do we drop the 'beg' attribute?
    """
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    logging.info("insertReading: %s", in_json)
    rc = 503
    jstr = None
    try:
        logging.info("about to execute")
        ddb_json = decode_json(in_json)
        ddb_json['CreatedAt'] = timestamp
        ddb_json['Id'] = bot_type + "-" + ddb_json['deviceid']
        db_table.put_item(Item=ddb_json)
        rc = 200
        #logging.info("class %s json - %s", type(ddb_json), ddb_json)
        jstr = str(ddb_json)
        #logging.info("commit complete")
    except Exception as db_exception:
        logging.exception(db_exception)
        rc = 500
        jstr = { "err" : json.loads(str(db_exception)) }

    return {
        "body": json.dumps(jstr),
        "statusCode" : rc,
        "headers": {
            "Content-Type" : "application/json",
        },
    }






def get_call(bot_type, jsonstr):
    """
    Does the GET request for the specific bot type and given request string
    """
    logging.info("get_call(%s, %s)" % (bot_type, jsonstr))

    jstr = None
    rc = 503
    try:

        if jsonstr is None:
            nrow = db_table.query(IndexName="BotTypeIndex", Select="COUNT", KeyConditionExpression=Key('bottype').eq(bot_type))['Count']
            rslt = db_table.query(IndexName="BotTypeIndex", ScanIndexForward=False, Limit=1, KeyConditionExpression=Key('bottype').eq(bot_type))['Items']
           
            jstr = {"cnt" : nrow,
                    "resource" : bot_type,
                    "lastUpdate": (rslt[0]['CreatedAt'] if len(rslt) > 0 else None)}
            rc = 200
        else:
            jstr = {"todo" : "retrun stuff associated with param", 
                    "param" : jsonstr['botid'] }

    except Exception as db_exception:
        logging.exception(db_exception)
        jstr = { "err" : str(db_exception) }


    logging.info("return string %s", json.dumps(jstr))
    return {
        "body": json.dumps(jstr),
        "statusCode" : rc,
        "headers": {
            "Content-Type" : "application/json",
        },
    }



def handle_dynabot(event, context):
    """
    Dynamic Bot REST endpoint to DynamoDB table

    Requires 'deviceid' to be present
      primary key - combination of '{bot_type}-{deviceid}'
      secondary key - new timestamp form at 'YYYY-MM-DD HH:mm:ss'
    """
    logging.info("debug: event: %s", event)

    
    operation = event['httpMethod']
    data = event['queryStringParameters'] if operation == 'GET' else json.loads(event['body'])

    bot_type = event['pathParameters']['bottype']

    logging.info("read the bottype: %s", bot_type)
    logging.debug("incoming data: %s", data)

    operations = {
        'POST' : lambda jsonstr, bot_type: post_call(bot_type, jsonstr),
        'GET' : lambda jsonstr, bot_type: get_call(bot_type, jsonstr)
    }


    # see if we can delegate the call
    if (operation in operations and bot_type in BOT_TYPES):
        return operations[operation](data, bot_type)

    logging.error("unknown method(%s) or resource(%s)", operation, resource)

    return {
        "body": {"message" : "unknown method(%s) or bot_type(%s)" % (operation, bot_type)},
        "statusCode" : 400,
        "headers": {
            "Content-Type" : "application/json",
        },
    }





def handle_dynabot1(event, context):
    """
    used for debugging
    """
    logging.info("debug: event: %s", event)
    logging.info("debug: context: %s", context)
    return {
        "body": json.dumps(event),
        "headers": {
            "Content-Type" : "application/json",
        },
    }

