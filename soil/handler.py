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


def openConnection():
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
    t = ( x['battery'],
          x['humidity'],
          x['soilmoisture1'],
          x['soilmoisture2'],
          x['soilmoisture3'],
          x['tempc'],
          x['tempf'],
          x['volts'],
          x['deviceid'])

    try:
        openConnection()
        cur = conn.cursor()
        logging.info("about to execute")
        cur.execute("INSERT INTO soil_bot (battery, humidity, soilmoisture1, soilmoisture2, soilmoisture3, tempc, tempf, volts, deviceid) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", t)
        logging.info("about to commit")
        conn.commit()
        logging.info("finihed commit")

    except Exception as e:
        logging.exception(e)
        # responseStatus = FAILD
    finally:
        if(conn is not None):
            conn.close()

    return json.dumps(t)


def getSoil(x):
    logging.info("nothing to see here")
    return [{ "beg" : "beg" }]


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
