#!/usr/bin/python
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

    except Exception as e:
        logging.error(e)
        raise e



def insertSoil(x):
    logging.info("insertSoil: %s", x)
    try:
        openConnection()
        cur = conn.cursor()
        logging.info("about to execute")
        cur.execute("INSERT INTO soil_bot (battery, humidity, soilmoisture1, soilmoisture2, soilmoisture3, tempc, tempf, volts, deviceid) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", x);
        logging.info("about to commit")
        conn.commit()
        logging.info("finihed commit")

    except Exception as e:
        logging.exception(e)
        # responseStatus = FAILD
    finally:
        if(conn is not None):
            conn.close()

    return { "beg" : "beg" }


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


def getTuple(x):
    ''' 
    get tuple to match
    (battery, humidity, soilmoisture1, soilmoisture2, soilmoisture3, tempc, tempf, volts, deviceid)
    '''

    return ( x['battery'],
             x['humidity'],
             x['soilmoisture1'],
             x['soilmoisture2'],
             x['soilmoisture3'],
             x['tempc'],
             x['tempf'],
             x['volts'],
             x['deviceid'])


raw_data = '{"tempc": 26.743469514692606, "tempf": 80.13824512644669, "deviceid": "1000aaaaffff0001", "volts": 5.013319587879101, "soilmoisture1": 3001.8796429352547, "soilmoisture2": 3002.6622931285337, "soilmoisture3": 1, "battery": 99.54414020769268, "beg": "beg", "humidity": 8.246388320176044}'


# TODO create Tuple to match SQL 


j = json.loads(raw_data)
print(j['volts'])
t = getTuple(j)
print(t)
openConnection()

insertSoil(t)
