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
import logging as log

import friendtube.parsers as rparse
import friendtube.querys as querys

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
                    #TODO: extend the token. Test if should be done here.
                    #extending = graph.extend_access_token(FACEBOOK_APP_ID,
                    #                                      FACEBOOK_APP_SECRET)
                    #log.debug("This is the new token: " + repr(extending))
                    #log.debug("this is the old one: " + cookie["access_token"])
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
            else:
                # This hits when the user has logged out
                log.warning("Have we been logged out?")
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

    def render(self, values = {}, template = "home.html"):
        """render the values in the template.
        by default it goes to the index page"""
        # There are some default values that we will always use
        values["facebook_app_id"]=FACEBOOK_APP_ID
        values["current_user"]=self.current_user
        # and then just load and render the template
        template = jinja_environment.get_template(template)
        self.response.out.write(template.render(values))

    def do_query(self, query = None, fql = False):
        """ Easy querying to facebook. It handles the errors and issues an
        retrieves just an empty dict with the errors if nothing returned.
        Returns a dict with the "data" and the "error" if any.
        """
        assert(query != None)
        result = { "data": []}
        error = ""

        try:
            graph = facebook.GraphAPI(self.current_user['access_token'])
            log.debug("Query: " + query)
            if fql:
                # Perform the fql query
                result = graph.fql(query)
            else:
                # Its a graph api query
                result = graph.get_object(query)
                log.debug( u"result"+ repr(result))
        except Exception as e:
            # GraphAPIError , and if there is expired, means that we need to relogin
            # GraphAPIError 606, and if there is "permission" means we have no rights
            log.exception(e)
            try:
                # try to guess if we run out of time
                if e.message.find(u"Session has expired") > 0 or e.message.find(u"the user logged out") > 0:
                    #thing = u"Please go to <a href=\"/\">home</a>, logout, and come back in"
                    log.warning(e.message)
                    log.warning("The user session expired. {name} by id {id}".format(
                        name = self.session["user"]["name"],
                        id = self.session["user"]["id"]))
                    # and we should try to relogin again or something
                    error = "Please relogin again"
                else:
                    log.warning("something bad happened or we are logged out")
                    raise
            except:
                #reraise
                raise

            # TODO: test here if we should return sample results or what. by
            # now, just empty
        return {"data":result["data"],"error":error}



    def get_video_listing(self, query = querys.filters_newsfeed):
        """ gets a list of videos and returns it as a list of thingis.
        To take a look at what kind of list and dicts we expect, take a 
        look at the parsers.py module in radiofaba
        """
        #query = querys.filters_newsfeed
        graph = facebook.GraphAPI(self.current_user['access_token'])
        try:
            log.debug("Query: " + query)
            # Perform the fql query
            result = graph.fql(query)
            video_list = rparse.parse_json_video_listing(result)
            result_parsed = rparse.clean_list(video_list)
            log.debug( u"result"+ repr(result))
            # GraphAPIError , and if there is expired, means that we need to relogin
            # GraphAPIError 606, and if there is "permission" means we have no rights
        except Exception as e:
            log.exception(e)
            try:
                # try to guess if we run out of time
                if e.message.find(u"Session has expired") > 0 or e.message.find(u"the user logged out") > 0:
                    #thing = u"Please go to <a href=\"/\">home</a>, logout, and come back in"
                    log.warning("The user session expired")
                    # and try to extend the session
                    #TODO: it does not work this way. delete this 
                    graph = facebook.GraphAPI(self.request.cookies)
                    extending = graph.extend_access_token(
                        FACEBOOK_APP_ID,
                        FACEBOOK_APP_SECRET)
                    result = graph.fql(query)
                    result_parsed = rparse.parse_json_video_listing(result)
                else:
                    log.warning("something bad happened")
                    raise
            except Exception as e:
                raise

            # then load the sample results
            import friendtube.sampleresult as smpl
            result_parsed = rparse.parse_json_video_listing(smpl.result)
        return result_parsed


class AdvancedListHandler(BaseHandler):
    def get(self, query = None, fql = False):
        if query == None:
            #Use the default query
            fblist = self.do_query(querys.filters_newsfeed, fql=True)
        else:
            fblist = self.do_query(query, fql)
        #TODO: Decide the final flow of the app. By now i keep both here.
        if fblist["error"] == "Please relogin again":
            error = self.redirect("/logout")  # If we detect logged out here, go home
        if fblist["data"] == []:
            # then load the sample results
            log.warning("Loading sample results")
            import friendtube.sampleresult as smpl
            listing = rparse.parse_json_video_listing(smpl.result)
        else:
            listing = rparse.parse_json_video_listing(fblist)
        # And render
        self.render(dict(
                        playlist = listing,
                        error = fblist["error"]
                    ),
                    "adv_player.html"
                    )

class OwnListHandler(AdvancedListHandler):
    def get(self):
        # we call the parent with other query.
        super(OwnListHandler, self).get(querys.fql_ownvideos , fql = True)


class ListHandler(BaseHandler):
    def get(self):
        try:    
            listing = self.get_video_listing()
            self.render(dict(
                playlist = listing
                ),
                "player.html")
        except Exception as e:
            log.exception(e)
            try:
                # try to guess if we run out of time
                if e.message.find(u"Session has expired") > 0 or e.message.find(u"the user logged out") > 0:
                    thing = u"Please go to <a href=\"/\">home</a>, logout, and come back in"
                else:
                    thing = u""
            except Exception as e:
                # nasty trick to at least give output
                import sys
                thing = rparse.nice_exception(e)

            # then load the sample results
            import friendtube.sampleresult as smpl
            listing = rparse.parse_json_video_listing(smpl.result)
            self.render(dict(
                            playlist = listing,
                            error = e,
                            thing = thing
                        ),
                        "player.html"
                        )


class HomeHandler(BaseHandler):
    def get(self):
        # We are going to get the list of friends and show it.
        friends = self.retrieve_friends()
        if friends["error"].find("relogin") >= 0:
            error = self.redirect("/logout")  # If we detect logged out here, go home
        self.render({"friends" : friends["data"], "error":friends["error"] })

    def retrieve_friends(self):
        friend_list = {"data": {}, "error":""}
        try:
            #Its common to fail getting friends if the user is logged out, so
            #ignore all exceptions
            friend_list = self.do_query(querys.graph_friends)
        except:
            pass # expected, as is normal to fail getting friends.

        return friend_list

    def post(self):
        """just to see what is POST ed """
        log.debug(self.request.get("signed_request"))
        try:
            # we use the facebook lib to parse the signed request
            fbdata = facebook.parse_signed_request(self.request.get("signed_request"),
                                                   FACEBOOK_APP_SECRET)
            log.debug( fbdata )
            # and we try to get the data of the user from our database
            current_user = User.get_by_key_name(fbdata["user_id"])
            if not current_user:
                # Not an existing user so say not implemented yet and failback 
                # to the normal page
                raise NotImplementedError, u"""This feature is in beta stage, login
                      first using the standalone app in <a
                      href="simpleapp-test.appspot.com>simpleapp-test.appspot.com</a>"""
            
            self.render()
        except Exception as e:
            extra_info = rparse.nice_exception(e)
            self.response.out.write(template.render(data  = """Sorry, we are
                                    still working on this, so there are some
                                                    errors like: <br />
                                                    {0}""".format(extra_info)))



class CanvasHandler(HomeHandler):
    def post(self):
        """handles the login process differently than HomeHandler, triggering it async"""
        log.debug("PARSING POST")
        self.render = super(HomeHandler,post,"canvas.html")
        #super(HomeHandler,post)



class LogoutHandler(BaseHandler):
    def get(self):
        if self.current_user is not None:
            self.session['user'] = None
        self.redirect('/')


class CanvasHandler(HomeHandler):
    def post(self):
        """handles the login process differently than HomeHandler, triggering it async"""
        log.debug("PARSING POST")
        self.render = super(HomeHandler,post,"canvas.html")
        #super(HomeHandler,post)


jinja_environment = jinja2.Environment(
        loader=jinja2.FileSystemLoader(
            os.path.dirname(__file__) + "/templates"))
log.debug("The path for templates is" +
              os.path.dirname(__file__) + "/templates")


app = webapp2.WSGIApplication(
    [('/', HomeHandler),
     ('/canvas', CanvasHandler),
     ('/canvas/', CanvasHandler),
     ('/list', ListHandler),
     ('/advlist', AdvancedListHandler),
     ('/ownlist', OwnListHandler),
     ('/logout', LogoutHandler)],
    debug=True,
    config=config
)
