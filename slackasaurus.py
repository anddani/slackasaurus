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
    print(parsed_request['text'])

    if 'text' in parsed_request:
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


def parse_request(request):
    if request is None:
        return {}
    return request
