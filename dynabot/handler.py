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
import json
import logging

import boto3
dynamodb = boto3.resource('dynamodb')

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)




# this will be a mapping to tables? (or will everything be in a single table???)
BOT_TYPES = {
    'soil' : 'soil_bot',
    'cure' : 'cure_bot',
    'aqua' : 'aqua_bot',
    'gas' : 'gas_bot',
    'light' : 'light_bot',
}


# I don't think this is needed
BOT_KEYS = {
    'soil' : ('battery', 'humidity', 'soilmoisture1', 'soilmoisture2', 'soilmoisture3', 'tempc', 'tempf', 'volts', 'deviceid'),
    'cure' : ('battery', 'humidity', 'infrared', 'uvindex', 'visible', 'tempc', 'tempf', 'volts', 'deviceid'),
    'aqua' : ('battery', 'ec', 'sal', 'sg', 'tds', 'ph', 'doxygen', 'tempc', 'tempf', 'volts', 'deviceid'),
    'gas' : ('battery', 'carbondioxide', 'volts', 'deviceid'),
    'light' : ('battery', 'humidity', 'infrared', 'fullspec', 'visible', 'lux', 'par', 'tempc', 'tempf', 'volts', 'deviceid'),
}



def get_tuple(in_dict, in_tuple):
    """
    generates an order tuple of values corresponding to the input key tuple
    """
    out_obj = ()
    for elem in in_tuple:
        if elem in in_dict:
            out_obj = out_obj + (in_dict[elem],)
        else:
            out_obj = out_obj + (None, )
    return out_obj





#def insertReading(in_json, in_keys, in_sql):
def post_call(bot_type, in_json):
    """
    generic function inserts keys from the json string
    """

    logging.info("insertReading: %s", in_json)
    data_vals = get_tuple(in_json, BOT_KEYS[bot_type])
    try:
        open_connection()
        cur = CONN.cursor()
        logging.info("about to execute")
        cur.execute(BOT_SQL_INS[bot_type], data_vals)
        CONN.commit()
        logging.info("commit complete")
    except Exception as sql_exception:
        logging.exception(sql_exception)
        # responseStatus = FAILD
    finally:
        if CONN is not None:
            CONN.close()

    return json.dumps(data_vals)







def get_call(bot_type, jsonstr):
    """
    Does the GET request for the specific bot type and given request string
    """
    logging.info("get_call(%s, %s)" % (bot_type, jsonstr))
    nrows = 0
    last_update = None
    try:
        open_connection()
        cur = CONN.cursor()
        cur.execute(SQL_CNT % BOT_TYPES[bot_type])
        nrows = cur.fetchone()[0]
        cur.execute(SQL_GET_LATEST % BOT_TYPES[bot_type])
        last_update = cur.fetchone()[0]
    except Exception as sql_exception:
        logging.exception(sql_exception)
        # responseStatus = 503
    finally:
        if CONN is not None:
            CONN.close()

    jstr = {"cnt" : nrows,
            "resource" : bot_type,
            "lastUpdate": (last_update.isoformat() if last_update is not None else None)}
    return jstr


def handle_dynabot(event, context):
    """
    used for debugging
    """
    data = event['queryStringParameters'] if operation == 'GET' else json.loads(event['body'])
    operation = event['httpMethod']

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    return {
        "body": json.dumps(event),
        "headers": {
            "Content-Type" : "application/json",
        },
    }




def handle_bot(event, context):
    '''  this is our handler code in the Lambda function
    REST interface for GET and POST
    '''
    resource = event['path'].split('/')[-1]
    # this is also event['pathParameter']['bottype']
    # got a key error here
    #logging.error("parsed %s", event['pathParameter']['bottype'])

    # get the first parameter from event
    operations = {
        'POST' : lambda jsonstr, bot_type: post_call(bot_type, jsonstr),
        'GET' : lambda jsonstr, bot_type: get_call(bot_type, jsonstr)
    }

    operation = event['httpMethod']
    if (operation in operations and resource in BOT_TYPES):
        payload = event['queryStringParameters'] if operation == 'GET' else json.loads(event['body'])
        response_code = 200
        body = operations[operation](payload, resource)
#        body = { 'resource' : ("%s" % resource), 'bottype' : bot_types[resource], 'event' : json.dumps(event) }
    else:
        logging.error("unknown method(%s) or resource(%s)", operation, resource)
        response_code = 503
        body = {"message" : "unknown method(%s) or resource(%s)" % (operation, resource)}

    return {
        "statusCode": response_code,
        "body": json.dumps(body),
        "headers": {
            "Content-Type" : "application/json",
        },
    }
