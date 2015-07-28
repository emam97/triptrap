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

class LoginHanlder(webapp2.RequestHandler):
    def get(self):
            greeting = ('<a href="%s">Sign in with Google</a>' %
                users.create_login_url('/main'))
            template_vars = { 'greeting' :  greeting }
            template = jinja2_environment.get_template('templates/triptrap.html')
            self.response.write(template.render(template_vars))



class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' %
            (user.nickname(), users.create_logout_url('/')))
        self.response.write('<html><body>%s</body></html>' % greeting)
        template = jinja2_environment.get_template("templates/places.html")
        self.response.write(template.render())

jinja2_environment = jinja2.Environment(loader=
jinja2.FileSystemLoader(os.path.dirname(__file__)))

app = webapp2.WSGIApplication([
    ('/', LoginHanlder),
    ('/main', MainHandler)
], debug=True)
