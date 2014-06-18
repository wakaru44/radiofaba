#!/usr/bin/env python
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""
A barebones AppEngine application that list videos posted by friends

more info on http://wiki.poli.nom.es/index.php/Facebook_and_yutul

"""

import sys
sys.path.append("./lib")
import webapp2
from os import path
import jinja2

import logging as log

from friendtube.HomeHandlers import HomeHandler, CanvasHandler, LogoutHandler
#from friendtube.HomeHandlers import TestHandler # deprecated, useless
from friendtube.ListHandlers import ListHandler, OwnListHandler

config = {}
config['webapp2_extras.sessions'] = dict(secret_key='')


app = webapp2.WSGIApplication(
    [('/', HomeHandler),
     ('/canvas', CanvasHandler),
     ('/canvas/', CanvasHandler),
     ('/list', ListHandler),
     ('/ownlist', OwnListHandler),
     #('/test', TestHandler),  # useless. deprecated
     ('/logout', LogoutHandler)],
    debug=True,
    config=config
)
