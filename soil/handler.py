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
        elif (not conn.open):
            conn = psycopg2.connect(host=rds_host, database=rds_dbname, user=rds_username, password=rds_password)

    except Exception as e:
        print(e)
        raise e



def insertSoil(x):
    logging.info("oh voi")


def getSoil():
    logging.info("nothing to see here")


def soil(event, context):
    '''  this is our handler code in the Lambd function
    REST interface for GET and POST
     see https://github.com/awslabs/serverless-application-model/blob/develop/examples/apps/microservice-http-endpoint-python3/lambda_function.py
    '''

    operations = {
        'POST' : lambda x: insertSoil(x),
        'GET': lambda x: getSoil(x)
    }

    part2 = "X"
    operation = event['httpMethod']
    if operation in operations:
        payload = event['queryStringParameters'] if operation == 'GET' else json.loads(event['body'])
        operations[operation](payload)
    else:
        part = "oh no, something wen wrong"

#    if (context.httpMethod && event.httpMethod == "GET") {
#        part2 = "some randome text"
#    }

    body = {
        "message": "Go soilbot successfully!",
        "part2" : payload,
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body),
        "headers": {
            "Content-Type" : "application/json",
        },
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Default return, something went wrong in soil handler",
        "event": event
    }
    """
