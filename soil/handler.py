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



def insertSoil(x):
    logging.info("insertSoil: %s", x)
#    t = ( x['battery'],
#          x['humidity'],
#          x['soilmoisture1'],
#          x['soilmoisture2'],
#          x['soilmoisture3'],
#          x['tempc'],
#          x['tempf'],
#          x['volts'],
#          x['deviceid'])
    t = getTuple(x, ('battery', 'humidity', 
                     'soilmoisture1', 'soilmoisture2', 'soilmoisture3',
                     'tempc', 'tempf', 'volts', 'deviceid'))

    try:
        openConnection()
        cur = conn.cursor()
        logging.info("about to execute")
        cur.execute("INSERT INTO soil_bot (created_at, battery, humidity, soilmoisture1, soilmoisture2, soilmoisture3, tempc, tempf, volts, deviceid) VALUES (now(), %s, %s, %s, %s, %s, %s, %s, %s, %s)", t)
        conn.commit()
        logging.info("commit complete")
    except Exception as e:
        logging.exception(e)
        # responseStatus = FAILD
    finally:
        if(conn is not None):
            conn.close()

    return json.dumps(t)


def getSoil(x):
    logging.info("getcount")
    nrows = 0
    try:
        openConnection()
        cur = conn.cursor()
        cur.execute("SELECT count(*) from soil_bot;")
        nrows = cur.fetchone()[0]
    except Exception as e:
        logging.exception(e)
        # responseStatus = FAILD
    finally:
        if(conn is not None):
            conn.close()

    jstr = { "cnt" : nrows }
    return jstr


def getResponse(body):
    ''' wraps the JSON body with appropriate response class
    '''
    return {
        "statusCode": 200,
        "body": json.dumps(body),
        "headers": {
            "Content-Type" : "application/json",
        },
    }








def soil(event, context):
    '''  this is our handler code in the Lambd function
    REST interface for GET and POST
     see https://github.com/awslabs/serverless-application-model/blob/develop/examples/apps/microservice-http-endpoint-python3/lambda_function.py
    '''

    operations = {
        'POST' : lambda x: insertSoil(x),
        'GET': lambda x: getSoil(x)
    }

    operation = event['httpMethod']
    if operation in operations:
        payload = event['queryStringParameters'] if operation == 'GET' else json.loads(event['body'])
        body = operations[operation](payload)
    else:
        logging.error("unknown method %s", operation)
        body = { "message" : "something went wrong" }

#    if (context.httpMethod && event.httpMethod == "GET") {
#        part2 = "some randome text"
#    }

#    body = {
#        "message": "Go soilbot successfully!",
#        "part2" : payload,
#        "input": event
#    }

    return getResponse(body)

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Default return, something went wrong in soil handler",
        "event": event
    }
    """
