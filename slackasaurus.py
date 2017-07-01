from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def get_root():
    print('GET request:')
    print(request)
    return '<h1>Hello from slackasaurus</h1>'


@app.route('/', methods=['POST'])
def post_root():
    print('POST request:')
    print(request)
    return '<h1>Hello from slackasaurus</h1>'
