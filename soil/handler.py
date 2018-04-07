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





def doCall(operations, event, context):
    """
    generic method to call with a set of mapped REST operations as input
    """
    operation = event['httpMethod']
    if operation in operations:
        payload = event['queryStringParameters'] if operation == 'GET' else json.loads(event['body'])
        responseCode = 200
        body = operations[operation](payload)
    else:
        logging.error("unknown method %s", operation)
        responseCode = 503
        body = { "message" : "something went wrong" }

    return {
        "statusCode": responseCode,
        "body": json.dumps(body),
        "headers": {
            "Content-Type" : "application/json",
        },
    }
    






def insertReading(in_json, in_keys, in_sql):
    """ 
    generic function inserts keys from the json string
    """

    logging.info("insertReading: %s", in_json)
    t = getTuple(in_json, in_keys)
    try:
        openConnection()
        cur = conn.cursor()
        logging.info("about to execute")
        cur.execute(in_sql, t)
        conn.commit()
        logging.info("commit complete")
    except Exception as e:
        logging.exception(e)
        # responseStatus = FAILD
    finally:
        if(conn is not None):
            conn.close()

    return json.dumps(t)




keys_soil = ( 'battery', 'humidity', 'soilmoisture1', 'soilmoisture2', 'soilmoisture3',
              'tempc', 'tempf', 'volts', 'deviceid')
sql_soil_ins = "INSERT INTO soil_bot (created_at, version, battery, humidity, soilmoisture1, soilmoisture2, soilmoisture3, tempc, tempf, volts, deviceid) VALUES (now(), 0, %s, %s, %s, %s, %s, %s, %s, %s, %s)"




keys_cure = ( 'battery', 'humidity', 'infrared', 'uvindex', 'visible',
              'tempc', 'tempf', 'volts', 'deviceid')
sql_cure_ins = "INSERT INTO cure_bot (created_at, version, battery, humidity, infrared, uvindex, visible, tempc, tempf, volts, deviceid) VALUES (now(), 0, %s, %s, %s, %s, %s, %s, %s, %s, %s)"



keys_aqua = ( 'battery', 'ec', 'sal', 'sg', 'tds', 'ph', 'doxygen',
              'tempc', 'tempf', 'volts', 'deviceid')
sql_aqua_ins = "INSERT INTO aqua_bot (created_at, version, battery, ec, sal, sg, tds, ph, doxygen, tempc, tempf, volts, deviceid) VALUES (now(), 0, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"



keys_gas = ( 'battery', 'carbondioxide',
              'volts', 'deviceid')
sql_gas_ins = "INSERT INTO gas_bot (created_at, version, battery, carbondioxide, volts, deviceid) VALUES (now(), 0, %s, %s, %s, %s)"


keys_light = ( 'battery', 'humidity', 'infrared', 'fullspec', 'visible', 'lux', 'par',
              'tempc', 'tempf', 'volts', 'deviceid')
sql_light_ins = "INSERT INTO light_bot (created_at, version, battery, humidity, infrared, fullspec, visible, lux, par, tempc, tempf, volts, deviceid) VALUES (now(), 0, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"








sql_cnt = "SELECT count(*) from %s"
sql_latest = "SELECT created_at from %s where created_at is not null order by created_at DESC limit 1"

def getCall(dbtable, x):
    logging.info("getCall(%s)" % (dbtable,))
    nrows = 0
    last_update = None
    try:
        openConnection()
        cur = conn.cursor()
        cur.execute(sql_cnt % dbtable)
        nrows = cur.fetchone()[0]
        cur.execute(sql_latest % dbtable)
        last_update = cur.fetchone()[0]
    except Exception as e:
        logging.exception(e)
        # responseStatus = 503
    finally:
        if(conn is not None):
            conn.close()

    jstr = { "cnt" : nrows, "lastUpdate": (last_update.isoformat() if last_update is not None else None) }
    return jstr








def soil(event, context):
    '''  this is our handler code in the Lambd function
    REST interface for GET and POST
     see https://github.com/awslabs/serverless-application-model/blob/develop/examples/apps/microservice-http-endpoint-python3/lambda_function.py
    '''

    operations = {
        'POST' : lambda x: insertReading(x, keys_soil, sql_soil_ins),
        'GET': lambda x: getCall('soil_bot', x)
    }
    return doCall(operations, event, context)




def cure(event, context):
    '''  this is our handler code in the Lambd function
    REST interface for GET and POST
    '''

    operations = {
        'POST' : lambda x: insertReading(x, keys_cure, sql_cure_ins),
        'GET': lambda x: getCall('cure_bot', x)
    }
    return doCall(operations, event, context)


def aqua(event, context):
    '''  this is our handler code in the Lambda function
    REST interface for GET and POST
    '''

    operations = {
        'POST' : lambda x: insertReading(x, keys_aqua, sql_aqua_ins),
        'GET': lambda x: getCall('aqua_bot', x)
    }
    return doCall(operations, event, context)





def gas(event, context):
    '''  this is our handler code in the Lambda function
    REST interface for GET and POST
    '''

    operations = {
        'POST' : lambda x: insertReading(x, keys_gas, sql_gas_ins),
        'GET': lambda x: getCall('gas_bot', x)
    }
    return doCall(operations, event, context)





def light(event, context):
    '''  this is our handler code in the Lambda function
    REST interface for GET and POST
    '''

    operations = {
        'POST' : lambda x: insertReading(x, keys_light, sql_light_ins),
        'GET': lambda x: getCall('light_bot', x)
    }
    return doCall(operations, event, context)






