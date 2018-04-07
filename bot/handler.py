import os
import json
import logging
# from https://github.com/jkehler/awslambda-psycopg2
import psycopg2


logger = logging.getLogger()
logger.setLevel(logging.INFO)

# rds settings
rds_host = os.environ['RDS_HOST']
rds_username = os.environ['RDS_USERNAME']
rds_password = os.environ['RDS_PASSWORD']
rds_dbname = os.environ['RDS_DBNAME']


bot_types = {
    'soil' : 'soil_bot',
    'cure' : 'cure_bot',
    'aqua' : 'aqua_bot',
    'gas' : 'gas_bot',
    'light' : 'light_bot',
}

keys_soil = ( 'battery', 'humidity', 'soilmoisture1', 'soilmoisture2', 'soilmoisture3', 'tempc', 'tempf', 'volts', 'deviceid')
sql_soil_ins = "INSERT INTO soil_bot (created_at, version, battery, humidity, soilmoisture1, soilmoisture2, soilmoisture3, tempc, tempf, volts, deviceid) VALUES (now(), 0, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

keys_cure = ( 'battery', 'humidity', 'infrared', 'uvindex', 'visible', 'tempc', 'tempf', 'volts', 'deviceid')
sql_cure_ins = "INSERT INTO cure_bot (created_at, version, battery, humidity, infrared, uvindex, visible, tempc, tempf, volts, deviceid) VALUES (now(), 0, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

keys_aqua = ( 'battery', 'ec', 'sal', 'sg', 'tds', 'ph', 'doxygen', 'tempc', 'tempf', 'volts', 'deviceid')
sql_aqua_ins = "INSERT INTO aqua_bot (created_at, version, battery, ec, sal, sg, tds, ph, doxygen, tempc, tempf, volts, deviceid) VALUES (now(), 0, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

keys_gas = ( 'battery', 'carbondioxide', 'volts', 'deviceid')
sql_gas_ins = "INSERT INTO gas_bot (created_at, version, battery, carbondioxide, volts, deviceid) VALUES (now(), 0, %s, %s, %s, %s)"

keys_light = ( 'battery', 'humidity', 'infrared', 'fullspec', 'visible', 'lux', 'par', 'tempc', 'tempf', 'volts', 'deviceid')
sql_light_ins = "INSERT INTO light_bot (created_at, version, battery, humidity, infrared, fullspec, visible, lux, par, tempc, tempf, volts, deviceid) VALUES (now(), 0, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

bot_keys = {
    'soil' : keys_soil,
    'cure' : keys_cure,
    'aqua' : keys_aqua,
    'gas' : keys_gas,
    'light' : keys_light,
}


bot_sql_ins = {
    'soil' : sql_soil_ins,
    'cure' : sql_cure_ins,
    'aqua' : sql_aqua_ins,
    'gas' : sql_gas_ins,
    'light' : sql_light_ins,
}

conn = None


def getTuple(in_dict, in_tuple):
    """
    generates an order tuple of values corresponding to the input key tuple
    """
    o = ()
    for elem in in_tuple:
        if (elem in in_dict):
            o = o + (in_dict[elem],)
        else:
            o = o + (None, )
    return o

def openConnection():
    """ 
    opens connection to DB for Postgre using psycopg2 lib
    """
    global conn
    try:
        if (conn is None):
            conn = psycopg2.connect(host=rds_host, database=rds_dbname, user=rds_username, password=rds_password)
        elif (conn.closed):
            conn = psycopg2.connect(host=rds_host, database=rds_dbname, user=rds_username, password=rds_password)

    except Exception as e:
        logging.exception(e)
        raise e





#def insertReading(in_json, in_keys, in_sql):
def postCall(bot_type, in_json):
    """ 
    generic function inserts keys from the json string
    """

    logging.info("insertReading: %s", in_json)
    t = getTuple(in_json, bot_keys[bot_type])
    try:
        openConnection()
        cur = conn.cursor()
        logging.info("about to execute")
        cur.execute(bot_sql_ins[bot_type], t)
        conn.commit()
        logging.info("commit complete")
    except Exception as e:
        logging.exception(e)
        # responseStatus = FAILD
    finally:
        if(conn is not None):
            conn.close()

    return json.dumps(t)







sql_cnt = "SELECT count(*) from %s"
sql_latest = "SELECT created_at from %s where created_at is not null order by created_at DESC limit 1"

def getCall(bot_type, jsonstr):
    """
    Does the GET request for the specific bot type and given request string
    """
    logging.info("getCall(%s, %s)" % (bot_type,jsonstr))
    nrows = 0
    last_update = None
    try:
        openConnection()
        cur = conn.cursor()
        cur.execute(sql_cnt % bot_types[bot_type])
        nrows = cur.fetchone()[0]
        cur.execute(sql_latest % bot_types[bot_type])
        last_update = cur.fetchone()[0]
    except Exception as e:
        logging.exception(e)
        # responseStatus = 503
    finally:
        if(conn is not None):
            conn.close()

    jstr = { "cnt" : nrows, 
             "resource" : bot_type,
             "lastUpdate": (last_update.isoformat() if last_update is not None else None) }
    return jstr


def handleBot1(event, context):
    """
    used for debugging
    """

    return {
        "body": json.dumps(event),
        "headers": {
            "Content-Type" : "application/json",
        },
    }




def handleBot(event, context):
    '''  this is our handler code in the Lambda function
    REST interface for GET and POST
    '''
    resource = event['path'].split('/')[-1]
    # this is also event['pathParameter']['bottype']
    # got a key error here
    #logging.error("parsed %s", event['pathParameter']['bottype'])

    # get the first parameter from event
    operations = {
        'POST' : lambda jsonstr, bot_type: postCall(bot_type, jsonstr),
        'GET' : lambda jsonstr, bot_type: getCall(bot_type, jsonstr)
    }

    operation = event['httpMethod']
    if (operation in operations and resource in bot_types):
        payload = event['queryStringParameters'] if operation == 'GET' else json.loads(event['body'])
        responseCode = 200
        body = operations[operation](payload, resource)
#        body = { 'resource' : ("%s" % resource), 'bottype' : bot_types[resource], 'event' : json.dumps(event) }
    else:
        logging.error("unknown method(%s) or resource(%s)", operation, resource)
        responseCode = 503
        body = { "message" : "unknown method(%s) or resource(%s)" % (operation, resource) }

    return {
        "statusCode": responseCode,
        "body": json.dumps(body),
        "headers": {
            "Content-Type" : "application/json",
        },
    }


