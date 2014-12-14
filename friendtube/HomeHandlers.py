#!/usr/bin/env python

import logging as log

import facebook

import friendtube.parsers as rparse # the dep on this is minimal
import friendtube.querys as querys
import BaseHandler as BS
from BaseHandler import LogoutException


home_template = "home-0.5.html"  # the normal home
post_template = "home.html"  #used by default in the post for home
canvas_template = "canvas-0.2.html"  # used for the facebook canvas page



class HomeHandler(BS.BaseHandler):
    def get(self):
        # We are going to get the list of friends and show it.
        try:
            friends = self.retrieve_friends()
            current_user = self.current_user
        except LogoutException as e:
            log.warning("The user is logged out")
            friends = {}
            friends["data"] = None
            friends["error"] = "Log in with your facebook id, and go to <a href=/list> the videos</a>"
            current_user = None
            # we should show the demo page anyway
        self.render({"friends" : friends["data"], "error":friends["error"] },
                    home_template,
                    user = current_user
                   )

    def retrieve_friends(self, user = None):
        """tries to get the list of friends"""
        if user == None:
            user = self.current_user
        friend_list = {"data": {}, "error":""}
        try:
            #Its common to fail getting friends if the user is logged out, so
            #ignore all exceptions
            friend_list = self.do_query(querys.graph_friends, fql = False, user = user)
        except:
            pass # expected, as is normal to fail getting friends.

        return friend_list

    def post(self, template = post_template):
        """just to see what is POST ed """
        #TODO: rewrite this completly
        # NOTE rewriting this in the canvas handler
        log.debug(self.request.get("signed_request"))
        log.debug("Passed: " + template)
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
            
            self.render(user = current_user)
        except Exception as e:
            log.error("Pokemon exception in HomeHandler")
            log.exception(e)
            import sys
            self.response.out.write(template.render(data  = """
                Sorry, we are still working on this, so there are some
                errors like: <br /> {0}
                """.format(repr(sys.exc_info()))
           ))


class DirectHomeHandler(HomeHandler):
    def get(self):
        """detects if the user is logged out or not. If its logged out, welcome
        page. If it's logged in, goes to /list or other"""
        try:
            friends = self.retrieve_friends()
            current_user = self.current_user
            self.redirect("/list")  # it will only redirect if we are logged in
        except LogoutException as e:
            log.warning("The user is logged out")
            friends = {}
            friends["data"] = None
            friends["error"] = "Log in with your facebook id, and go to <a href=/list> the videos</a>"
            current_user = None
            # we should show the demo page anyway
        self.render({"friends" : friends["data"], "error":friends["error"] },
                    home_template,
                    user = current_user
                   )



class LogoutHandler(BS.BaseHandler):
    def get(self):
        try:
            if self.current_user is not None:
                self.session['user'] = None
        except LogoutException:
            pass  # expected
        self.redirect('/')


class CanvasHandler(HomeHandler):
    def get(self):
        try:
            self.render({"data" : repr(self.request.params), "error":"errorerror" },
                    canvas_template,
                    user = self.current_user)
        except:
            self.render({}, home_template)

    def post(self):
        """handles the login process differently than HomeHandler, triggering it async"""
        try:
            log.debug("PARSING POST")
            log.debug(dir(super(HomeHandler)))
            log.debug(super(HomeHandler))
            self.render({"data":self.request.params}, canvas_template, user = self.current_user)
        except:
            self.redirect("/list")
