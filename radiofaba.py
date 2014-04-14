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
FACEBOOK_APP_ID = "522368114539124"
FACEBOOK_APP_SECRET = "e75e283da7fc04b8e752e25a9459ed7e"

import sys
sys.path.append("./lib")
import facebook
import webapp2
import os
import jinja2
import urllib2

from google.appengine.ext import db
from webapp2_extras import sessions

import rfbtools.parsers as rparse

config = {}
config['webapp2_extras.sessions'] = dict(secret_key='')


class User(db.Model):
    id = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now=True)
    name = db.StringProperty(required=True)
    profile_url = db.StringProperty(required=True)
    access_token = db.StringProperty(required=True)


class BaseHandler(webapp2.RequestHandler):
    """Provides access to the active Facebook user in self.current_user

    The property is lazy-loaded on first access, using the cookie saved
    by the Facebook JavaScript SDK to determine the user ID of the active
    user. See http://developers.facebook.com/docs/authentication/ for
    more information.
    """
    @property
    def current_user(self):
        if self.session.get("user"):
            # User is logged in
            return self.session.get("user")
        else:
            # Either used just logged in or just saw the first page
            # We'll see here
            cookie = facebook.get_user_from_cookie(self.request.cookies,
                                                   FACEBOOK_APP_ID,
                                                   FACEBOOK_APP_SECRET)
            if cookie:
                # Okay so user logged in.
                # Now, check to see if existing user
                user = User.get_by_key_name(cookie["uid"])
                if not user:
                    # Not an existing user so get user info
                    graph = facebook.GraphAPI(cookie["access_token"])
                    profile = graph.get_object("me")
                    user = User(
                        key_name=str(profile["id"]),
                        id=str(profile["id"]),
                        name=profile["name"],
                        profile_url=profile["link"],
                        access_token=cookie["access_token"]
                    )
                    user.put()
                elif user.access_token != cookie["access_token"]:
                    user.access_token = cookie["access_token"]
                    user.put()
                # User is now logged in
                self.session["user"] = dict(
                    name=user.name,
                    profile_url=user.profile_url,
                    id=user.id,
                    access_token=user.access_token
                )
                return self.session.get("user")
        return None

    def dispatch(self):
        """
        This snippet of code is taken from the webapp2 framework documentation.
        See more at
        http://webapp-improved.appspot.com/api/webapp2_extras/sessions.html

        """
        self.session_store = sessions.get_store(request=self.request)
        try:
            webapp2.RequestHandler.dispatch(self)
        finally:
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        """
        This snippet of code is taken from the webapp2 framework documentation.
        See more at
        http://webapp-improved.appspot.com/api/webapp2_extras/sessions.html

        """
        return self.session_store.get_session()


def get_raw_listing(user = None):
    """ gets a list of videos and returns it as a list of thingis.
    To take a look at what kind of list and dicts we expect, take a 
    look at the parsers.py module in radiofaba
    """
    assert(user != None)
    # query = """SELECT message, attachment.href  FROM stream WHERE source_id in
    # (SELECT uid2 from friend WHERE uid1 == me())  and strpos(attachment.href,
    # "youtu") >= 0 LIMIT 100"""
    query = """SELECT message, attachment.href, attachment.name,
    attachment.description, message, attachment.icon, attachment  FROM stream
    WHERE source_id in
        (SELECT uid2 from friend WHERE uid1 == me())  and
        strpos(attachment.href,
            "youtu") >= 0 LIMIT 50"""
    graph = facebook.GraphAPI(user['access_token'])
    result = graph.fql(query)
    # TODO error handling
    # GraphAPIError , and if there is expired, means that we need to relogin
    # GraphAPIError 606, and if there is "permission" means we have no rights
    print("DEBUG:","XXXXXX type of response:", type(result))
    return result


def get_video_listing(user = None):
    """ gets a list of videos and returns it as a list of thingis.
    To take a look at what kind of list and dicts we expect, take a 
    look at the parsers.py module in radiofaba
    """
    assert(user != None)
    #query = """SELECT message, attachment.href  FROM stream WHERE source_id in
    #(SELECT uid2 from friend WHERE uid1 == me())  and strpos(attachment.href,
    #"youtu") >= 0 LIMIT 100"""
    query = """SELECT message, attachment.href, attachment.name,
    attachment.description, message, attachment.icon, attachment  FROM stream
    WHERE source_id in
        (SELECT uid2 from friend WHERE uid1 == me())  and
        strpos(attachment.href,
            "youtu") >= 0 LIMIT 100"""
    graph = facebook.GraphAPI(user['access_token'])
    result = graph.fql(query)
    print("DEBUG:", "result", dir(result))
    print("DEBUG:", "result", result)
    # TODO error handling
    # GraphAPIError , and if there is expired, means that we need to relogin
    # GraphAPIError 606, and if there is "permission" means we have no rights
    return rparse.parse_json_video_listing(result)


class ListHandler(BaseHandler):
    def get(self):
        template = jinja_environment.get_template('templates/player.html')
#        try:
#            listing = get_video_listing(self.current_user)
#        except:
#            listing = [] # TODO this is intentional for DEBUG

        listing = get_video_listing(self.current_user)
            
        self.response.out.write(template.render(dict(
            facebook_app_id=FACEBOOK_APP_ID,
            current_user=self.current_user,
            #thing = repr(get_raw_listing(self.current_user)),
            playlist = listing

        )))


class HomeHandler(BaseHandler):
    def get(self):
        template = jinja_environment.get_template('templates/home.html')
        self.response.out.write(template.render(dict(
            facebook_app_id=FACEBOOK_APP_ID,
            current_user=self.current_user
        )))


class LogoutHandler(BaseHandler):
    def get(self):
        if self.current_user is not None:
            self.session['user'] = None
        self.redirect('/')

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__))
)

app = webapp2.WSGIApplication(
    [('/', HomeHandler),
     ('/list', ListHandler),
     ('/logout', LogoutHandler)],
    debug=True,
    config=config
)
