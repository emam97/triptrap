#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from google.appengine.api import users
import webapp2
import jinja2
import os
import datetime
import logging
import urllib2
import json
from google.appengine.ext import ndb
import argparse
import pprint
import sys
import urllib
import oauth2

API_HOST = 'api.yelp.com'
DEFAULT_TERM = 'dinner'
DEFAULT_LOCATION = 'Atlanta, GA'
SEARCH_LIMIT = 6
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
def search(term, ll):
    """Query the Search API by a search term and location.
    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.
    Returns:
        dict: The JSON response from the request.
    """
    url_params = {
        'term': term.replace(' ', '+'),
        'll': ll.replace( ' ', ' , '),
        'limit': SEARCH_LIMIT
    }
    print url_params
    return request(API_HOST, SEARCH_PATH, url_params=url_params)

class Restraunt(ndb.Model):
    name = ndb.StringProperty()
    url = ndb.StringProperty()
    address = ndb.StringProperty()
    city = ndb.StringProperty()
    state = ndb.StringProperty()
    categories = ndb.StringProperty(repeated=True)
    types = ndb.StringProperty()

# class Location(ndb.Model):
#     latitude = ndb.FloatProperty()
#     longitude = ndb.FloatProperty()
#     created = ndb.DateTimeProperty()


class YelpHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja2_environment.get_template('template/yelp.html')
        rlist = []
        ll = self.request.get('lat')
        logging.info(ll)
        response = search('dinner', ll)
        for i in range(0, len(response)):
            r = Restraunt()
            a = response['businesses'][i]
            r.name = a['name']
            r.url = a['url']
            r.address = a['location']['display_address'][0]
            r.city = a['location']['display_address'][1]
            r.state = a['location']['display_address'][2]
            r.categories = a['categories'][0]
            logging.info(a['categories'][0])
            for b in range (0, len(r.categories)):
                r.types = a['categories'][0][b]
                break
            rlist.append(r)
        template_var = {
        'restruants' : rlist
         }
        self.response.write(template.render(template_var))


class EventfulHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja2_environment.get_template('template/eventful.html')
        lat = self.request.get('lat')
        lon = self.request.get('lon')
        url = ('http://api.eventful.com/json/events/search?app_key=TpFKjZjQc76tZrpF&where=%s,%s&within=25' % (lat,lon))
        r=urllib2.urlopen( url )
        s= r.read()
        d= json.loads(s)
        # logging.info(lat)
        # logging.info(lon)
        # if lat == "" or lon == "":
        #     form = True
        # else:
        #     form = False
        #     loc = Location(latitude = float(lat), longitude=float(lon),
        #     created=datetime.datetime.now())
        #     loc.put()
        for x in d["events"]["event"]:
            self.response.write(x["title"].encode("utf-8"))
            self.response.write(", ")
            self.response.write(x["venue_address"])
            self.response.write(", ")
            self.response.write(x["city_name"])
            self.response.write(", ")
            self.response.write(x["region_name"])
            self.response.write(", ")
            self.response.write(x["country_name"])
            self.response.write('</br>')

        self.response.write(template.render())


class LoginHanlder(webapp2.RequestHandler):
    def get(self):
            greeting = ('<a href="%s">Sign in with Google</a>' %
                users.create_login_url('/main'))
            template_vars = { 'greeting' :  greeting }
            template = jinja2_environment.get_template('template/triptrap.html')
            self.response.write(template.render(template_vars))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' %
            (user.nickname(), users.create_logout_url('/')))
        template_vars = { 'greeting' : greeting }
        template = jinja2_environment.get_template("template/directions.html")
        self.response.write(template.render(template_vars))

jinja2_environment = jinja2.Environment(loader=
jinja2.FileSystemLoader(os.path.dirname(__file__)))

app = webapp2.WSGIApplication([
    ('/', LoginHanlder),
    ('/main', MainHandler),
    ('/eventful', EventfulHandler),
    ('/yelp', YelpHandler)
], debug=True)
