import json
try:
    import urllib.request as urlrequest
except ImportError:
    import urllib2 as urlrequest


class Slackeratops:
    def __init__(self, url):
        self.url = url

    def post(self, data):
        request = urlrequest.Request(self.url,
                                     json.dumps(data).encode('utf--8'))
        request.add_header('Content-Type',  'application/json')

        response = urlrequest.urlopen(request)
        return response
