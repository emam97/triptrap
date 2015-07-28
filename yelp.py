import webapp2
import jinja2
import argparse
import json
import pprint
import sys
import urllib
import urllib2
import oauth2
import os
import logging

API_HOST = 'api.yelp.com'
DEFAULT_TERM = 'dinner'
DEFAULT_LOCATION = 'Atlanta, GA'
SEARCH_LIMIT = 4
SEARCH_PATH = '/v2/search/'
BUSINESS_PATH = '/v2/business/'

# OAuth credential placeholders that must be filled in by users.
CONSUMER_KEY = 'F6R9r8flzEZJZZxOd-KpMg'
CONSUMER_SECRET = '0qZ2wcKfMG56pGSyJmLatyz81XY'
TOKEN = 't-la5t5chvatXTSsDh7bHxzFMhfT92Gl'
TOKEN_SECRET = 'f3fipu1Ym_YulH3n2dQ53HHoG3E'

def request(host, path, url_params=None):
    """Prepares OAuth authentication and sends the request to the API.

    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        url_params (dict): An optional set of query parameters in the request.

    Returns:
        dict: The JSON response from the request.

    Raises:
        urllib2.HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = 'http://{0}{1}?'.format(host, urllib.quote(path.encode('utf8')))

    consumer = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
    oauth_request = oauth2.Request(method="GET", url=url, parameters=url_params)

    oauth_request.update(
        {
            'oauth_nonce': oauth2.generate_nonce(),
            'oauth_timestamp': oauth2.generate_timestamp(),
            'oauth_token': TOKEN,
            'oauth_consumer_key': CONSUMER_KEY
        }
    )
    token = oauth2.Token(TOKEN, TOKEN_SECRET)
    oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
    signed_url = oauth_request.to_url()


    conn = urllib2.urlopen(signed_url, None)
    try:
        response = json.loads(conn.read())
    finally:
        conn.close()
    return response
def search(term, location):
    """Query the Search API by a search term and location.
    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.
    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT
    }
    return request(API_HOST, SEARCH_PATH, url_params=url_params)

class YelpHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('template/triptrap.html')
        a = self.request.get('term')
        b = 'Atlanta'
        response = search(a,b)
        result = response['businesses'][0]
        name = result['name']
        url = result['url']
        address = result['location']
        categories = result['categories']
        template_var = { 'value1' : name, 'value2' : url,
        'value3' : address, 'value4' : categories
        }
        self.response.write(template.render(template_var))


jinja_environment = jinja2.Environment(loader=
    jinja2.FileSystemLoader(os.path.dirname(__file__)))

app = webapp2.WSGIApplication([
    ('/', YelpHandler)
], debug=True)
