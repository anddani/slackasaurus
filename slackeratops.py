import json
try:
    import urllib.request as urlrequest
except ImportError:
    import urllib2 as urlrequest


class Slackeratops:
    def __init__(self, url):
        self.url = url

    def post(self, data):
        encoded_data = json.dumps(data).encode('utf-8')
        request = urlrequest.Request(self.url,
                                     encoded_data)
        request.add_header('Content-Type',  'application/json')

        response = urlrequest.urlopen(request)
        return response
