import json


def soil(event, context):
    part2 = "X"
    operation = event['httpMethod']
    payload = event['queryStringParameters'] if operation == 'GET' else json.loads(event['body'])
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
