import json


def soil(event, context):
    part2 = "X"
#    if (context.httpMethod && event.httpMethod == "GET") {
#        part2 = "some randome text"
#    }

    if (event.headers != null) {
        part2 = "Y";
    }

    body = {
        "message": "Go soilbot successfully!",
        "part2" : part2,
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": JSON.stringify(body)
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
