from flask import Flask
from flask import request
from flask import make_response
import json

app = Flask(__name__)


@app.route('/', methods=['POST'])
def post_root():
    body = json.dumps(request.get_json(silent=True, force=True), indent=4)

    print('POST body:')
    print(body)
    response = make_response(body)
    response.headers['Content-Type'] = 'application/json'
    return response
