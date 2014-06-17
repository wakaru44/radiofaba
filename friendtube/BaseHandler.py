#!/usr/bin/env python

from os import path
import logging as log
import facebook
import webapp2
from webapp2_extras import sessions
import jinja2
from google.appengine.ext import db
from google.appengine.api.app_identity import get_application_id

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


class LogoutException(Exception):
    def __init__(self,*vars,**kwds):
        super(Exception,self).__init__(*vars,**kwds)


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
                raise LogoutException("mesa logged out tusa")
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

    def render(self, values = {}, template = "home.html", user = None):
        """render the values in the template.
        by default it goes to the index page"""
        # There are some default values that we will always use
        values["facebook_app_id"]=FACEBOOK_APP_ID
        # But the user has to be injected
        values["current_user"]=user
        # and then just load and render the template
        template = jinja_environment.get_template(template)
        self.response.out.write(template.render(values))

    def do_query(self, query = None, fql = False, user = None):
        """ Easy querying to facebook. It handles the errors and issues an
        retrieves just an empty dict with the errors if nothing returned.
        Returns a dict with the "data" and the "error" if any.
        """
        assert(query != None)
        result = { "data": []}
        error = ""

        try:
            if user  == None:
                # then try with the self property
                user = self.current_user
            if user == None:
                # then its definetly logout
                raise LogoutException("doing query") # send logout upstream
                                                       # and catch it up
            else:
                cu = user
            graph = facebook.GraphAPI(cu["access_token"])
            log.debug("doing Query: " + query)
            if fql:
                # Perform the fql query
                result = graph.fql(query)
            else:
                # Its a graph api query
                result = graph.get_object(query)
                ##log.debug( u"result"+ repr(result))
        except LogoutException as e:
            log.exception(e)
            raise # this should be catched the later the better, on the caller
                  # that decides the flow ofthe application
        except Exception as e:
            # GraphAPIError , and if there is expired, means that we need to relogin
            # GraphAPIError 606, and if there is "permission" means we have no rights
            log.debug("pokemon exception")
            log.exception(e)
            try:
                # try to guess if we run out of time
                if e.message.find(u"Session has expired") > 0 or e.message.find(u"user logged out") > 0:
                    #thing = u"Please go to <a href=\"/\">home</a>, logout, and come back in"
                    log.warning(e.message)
                    raise LogoutException("the query resulted in finished session")
                else:
                    log.warning("something bad happened")
                    log.warning(e.message)
                    log.warning("Silencing exception")
                    error = e.message
            except:
                #reraise
                raise

        return {"data":result["data"],"error":error}



