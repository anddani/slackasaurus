from flask import Flask
from flask import make_response
from flask import request

from slackeratops import Slackeratops

import json
import logging
import os

"""
TODO:
    - Have slack_post() return the appropriate response
    - Parse request from API.AI to find user, channel and message
"""

slack = Slackeratops(os.environ["SLACK_URL"])
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)


@app.route('/', methods=['POST'])
def slack_post():
    request_body = request.data

    logging.debug('POST body:')
    logging.debug(request_body)

    # Parse the request body to find the user, channel and message.
    parsed_request = parse_request(json.loads(request_body))
    print("Parsed request: ", parsed_request)

    # if 'text' in parsed_request:
    logging.debug(parsed_request)
    slack.post(parsed_request)

    # TODO: Appropriate response
    # For now, we return the parsed request (what is sent to slack)
    response_body = json.dumps(parsed_request)

    logging.debug('response body:')
    logging.debug(response_body)

    response = make_response(response_body)
    response.headers['Content-Type'] = 'application/json'

    return response


# TODO: Move this to another class
def parse_request(request):
    parsed_request = {}
    try:
        messages = request['result']['fulfillment']['messages']
    except KeyError:
        logging.debug('Invalid request JSON')
    else:
        slack_messages = list(filter(lambda x:
                                     'platform' in x and
                                     x['platform'] == 'slack' and
                                     x['type'] == 4, messages))
        if slack_messages and 'payload' in slack_messages[0]:
            parsed_request = slack_messages[0]['payload']

    return parsed_request

    # if request is None:
    #     return {}
    # if 'result' not in request:
    #     return {}
    # result = request['result']
    # print(result)
    # if 'fulfillment' not in result:
    #     return {}
    # fulfillment = result['fulfillment']
    # print(fulfillment)
    # if 'messages' not in fulfillment:
    #     return {}
    # messages = fulfillment['messages']
    # print(messages)
    # slack_messages = list(filter(lambda x: 'platform' in x and x['platform'] == 'slack' and x['type'] == 4, messages))
    # if not slack_messages:
    #     return {}
    # message = slack_messages[0]
    # if 'payload' not in message:
    #     return {}
    # return {'payload': message['payload']}

    # return message['payload']
