#!/usr/bin/env python

from os import path
import logging as log
import facebook
import webapp2
from webapp2_extras import sessions
import jinja2
from google.appengine.ext import db
from google.appengine.api.app_identity import get_application_id
import friendtube.querys as querys #TODO: try to remove this import 
import friendtube.parsers as rparse

FACEBOOK_APP_ID = "522368114539124"
FACEBOOK_APP_SECRET = "e75e283da7fc04b8e752e25a9459ed7e"

jinja_environment = jinja2.Environment(
        loader=jinja2.FileSystemLoader(
            path.dirname(__file__) + "/../templates"))
log.debug("The path for templates is" +
              path.dirname(__file__) + "/../templates")


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
        log.warning("The instance was called from: " + self.app.active_instance.request.application_url)
        log.warning("The instance was called from: " + get_application_id())
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
                log.warning("user logged out")
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
            log.debug("do Query: " + query)
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
                    log.warning(e.message)
                    log.warning("Silencing exception")
                    #TODO: We should redirect to logout, just to check.
                    # Somehow, it seems to be a bad idea.
                    #error = "Please relogin again"
                    #But raising is also harmful.
                    #raise
            except:
                #reraise
                raise

            # TODO: test here if we should return sample results or what. by
            # now, just empty
        return {"data":result["data"],"error":error}



    def get_video_listing(self, query = querys.filters_newsfeed):
        """ gets a list of videos and returns it as a list of thingis.
        To take a look at what kind of list and dicts we expect, take a 
        look at the parsers.py module in friendtube
        DEPRECATED. now we prefer do_query
        """
        #query = querys.filters_newsfeed
        graph = facebook.GraphAPI(self.current_user['access_token'])
        try:
            log.debug("get video listing Query: " + query)
            # Perform the fql query
            result = graph.fql(query)
            log.debug( u"result from get_video_listing: "+ repr(result.called))
            video_list = rparse.parse_json_video_listing(result)
            result_parsed = rparse.clean_list(video_list)
            log.debug( u"result from get_video_listing: "+ repr(result))
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


