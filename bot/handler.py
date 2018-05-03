"""
handler.py

author: matt cliff
created: april 8, 2018

AWS lambda python 3.6 code
provides RESTful endpoint to /api/metrics/{bottype}
for: soil, cure, aqua, gas, and light bots
  
"""
import os
import json
import logging
# from https://github.com/jkehler/awslambda-psycopg2
import psycopg2
from datetime import date, datetime


LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

CONN = None

# rds settings
RDS_HOST = os.environ['RDS_HOST']
RDS_USERNAME = os.environ['RDS_USERNAME']
RDS_PASSWORD = os.environ['RDS_PASSWORD']
RDS_DBNAME = os.environ['RDS_DBNAME']


BOT_TYPES = {
    'soil' : 'soil_bot',
    'cure' : 'cure_bot',
    'aqua' : 'aqua_bot',
    'gas' : 'gas_bot',
    'light' : 'light_bot',
}

BOT_KEYS = {
    'soil' : ('battery', 'humidity', 'soilmoisture1', 'soilmoisture2', 'soilmoisture3', 'tempc', 'tempf', 'volts', 'deviceid'),
    'cure' : ('battery', 'humidity', 'infrared', 'uvindex', 'visible', 'tempc', 'tempf', 'volts', 'deviceid'),
    'aqua' : ('battery', 'ec', 'sal', 'sg', 'tds', 'ph', 'doxygen', 'tempc', 'tempf', 'volts', 'deviceid'),
    'gas' : ('battery', 'carbondioxide', 'volts', 'deviceid'),
    'light' : ('battery', 'humidity', 'infrared', 'fullspec', 'visible', 'lux', 'par', 'tempc', 'tempf', 'volts', 'deviceid'),
}




class MyEncoder(json.JSONEncoder):
    """ JSON serializer for objects not serializable by default """
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat(' ', 'seconds')  #python3
        return json.JSONEncoder.default(self, obj)

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


def open_connection():
    """
    opens connection to DB for Postgre using psycopg2 lib
    """
    global CONN
    try:
        if CONN is None:
            CONN = psycopg2.connect(host=RDS_HOST, database=RDS_DBNAME,
                                    user=RDS_USERNAME, password=RDS_PASSWORD)
        elif CONN.closed:
            CONN = psycopg2.connect(host=RDS_HOST, database=RDS_DBNAME,
                                    user=RDS_USERNAME, password=RDS_PASSWORD)

    except Exception as sql_exception:
        logging.exception(sql_exception)
        raise sql_exception





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
        sql_stmt = ''.join(['INSERT INTO ', BOT_TYPES[bot_type], ' (created_at, version, ',
                   ', '.join(BOT_KEYS[bot_type]),  ') VALUES (now(), 0',
                   ', %s' * len(BOT_KEYS[bot_type]), ')'])

        cur.execute(sql_stmt, data_vals)
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
    device_id = None
    jstr = None

    try:
        open_connection()
        cur = CONN.cursor()


        if jsonstr is None:
            """ 
            make the no-param call to get count
            """

            cur.execute('SELECT count(*) FROM %s' % BOT_TYPES[bot_type])  # use %, part of SQL statement
            nrows = cur.fetchone()[0]

            sql_stmt = 'SELECT created_at, deviceid from %s where created_at is not null order by created_at DESC limit 1' % BOT_TYPES[bot_type] 
            cur.execute(sql_stmt)
            r_row = cur.fetchone()
            last_update = r_row[0]
            device_id = r_row[1]


            jstr = {"count" : nrows,
                    "deviceid" : device_id,
                    "CreatedAt": (last_update.isoformat(' ', 'seconds') if last_update is not None else None)}

        elif 'deviceid' in jsonstr.keys():
            """ 
            get all the data for the device
            """

            sql_stmt = ''.join(['SELECT created_at, version, ',
                       ', '.join(BOT_KEYS[bot_type]), ' FROM ',
                       BOT_TYPES[bot_type], ' WHERE deviceid = %s'])

            if 'startdate' in jsonstr.keys():
                """ 
                get all the data for the device
                """
                

                cur.execute(''.join([sql_stmt, ' AND created_at > %s']), (jsonstr['deviceid'], jsonstr['startdate']))

            else:
                """ 
                get all the data for the device
                """
                cur.execute(sql_stmt, (jsonstr['deviceid'],))

            rslt = cur.fetchall()

            logging.info("pulled back %s records from database", len(rslt));

            # the 0th elem is created_at
            # the rest match BOT_KEYS[bot_type]
            dict_names = ('CreatedAt', ) + BOT_KEYS[bot_type]
            jstr = list(map(lambda x: dict(zip(dict_names, x)), rslt))
            #logging.info("****Jstr", json.dumps(jstr, cls=MyEncoder));

        else:
            jstr = {"message" : "unknown paramater string" }





    except Exception as sql_exception:
        logging.exception(sql_exception)
        # responseStatus = 503
    finally:
        if CONN is not None:
            CONN.close()

    if jstr is None:
        jstr = { "message": "something went wrong" }


    return jstr


def handle_bot_debug(event, context):
    """
    used for debugging
    """

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
        "body": json.dumps(body, cls=MyEncoder),
        "headers": {
            "Content-Type" : "application/json",
        },
    }

