from flask import Flask
from flask import make_response
from flask import redirect
from flask import request

from slackeratops import Slackeratops

import json
import logging
import os

"""
TODO:
    - Have slack_post() return the appropriate response back to API.AI
    - Store lateness message from user
"""

slack = Slackeratops(os.environ["SLACK_URL"])
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

@app.route('/auth', methods=['GET'])
def secure_oauth():
    redirect_uri = request.args.get('redirect_uri')
    state = request.args.get('state')
    print(redirect_uri, state)
    return redirect('%s#access_token=abc123&token_type=bearer&state=%s' % (redirect_uri, state), code=302)

@app.route('/', methods=['POST'])
def slack_post():
    request_body = request.data

    logging.debug('POST request body: ')
    logging.debug(request_body)

    # Parse the request body from API.AI to find the user, channel and message.
    parsed_request = parse_request(json.loads(request_body))

    logging.debug('Parsed request:')
    logging.debug(parsed_request)

    if parsed_request:
        try:
            if parsed_request['username']:
                # Post message from API.AI to slack
                slack.post(parsed_request)
                # For now, we return the parsed request (what is sent to slack)
                response_body = json.dumps(parsed_request)
        except KeyError:
            # Return intent asking for user's name
            response_body = """
            {
              "expectUserResponse": true,
              "expectedInputs": [{
                "inputPrompt": {
                  "richInitialPrompt": {
                    "items": [{
                      "simpleResponse": {
                        "textToSpeech": "Give us your name"
                      }
                    }]
                  },
                  "noInputPrompts": []
                },
                "possibleIntents": [{
                  "intent": "actions.intent.PERMISSION",
                  "inputValueData": {
                    "@type": "type.googleapis.com/google.actions.v2.PermissionValueSpec",
                    "permissions": [ "NAME" ]
                  }
                }]
              }]
            }
            """


    logging.debug('Response body:')
    logging.debug(response_body)

    response = make_response(response_body)
    response.headers['Content-Type'] = 'application/json'

    return response


def parse_request(request):
    """
    {
      ...
      "result": {
        ...
        "fulfillment": {
          "messages": [
            {
              "type": 0,
              "platform": "slack",
              "speech": "Alright, I'll tell your coworkers that you will be 7 h late."
            },
            {
              "type": 4,
              "platform": "slack",
              "payload": {
                "icon_emoji": ":crocodile:",
                "username": "bontosaurus",
                "text": ["I will be 7 h late becuase reason", "I will be 7 h late"]
              }
            },
            {
              "type": 0,
              "speech": "Alright, I'll tell your coworkers that you will be 7 h late."
            }
          ]
        }
      },
        ...
    }
    """
    parsed_request = {}
    try:
        messages = request['result']['fulfillment']['messages']
    except KeyError:
        logging.error('Invalid request JSON')
    else:
        slack_messages = list(filter(lambda x:
                                     'payload' in x, messages))
        if slack_messages:
            parsed_request = slack_messages[0]['payload']
            non_empty = [x for x in parsed_request['text'] if x]
            parsed_request['text'] = non_empty[0] if non_empty else ""


    return parsed_request
