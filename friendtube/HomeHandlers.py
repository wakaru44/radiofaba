#!/usr/bin/env python


import logging as log

import facebook

import friendtube.parsers as rparse
import friendtube.querys as querys
#from friendtube import BaseHandler
import BaseHandler as BS



class HomeHandler(BS.BaseHandler):
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

    def post(self, template = "home.html"):
        """just to see what is POST ed """
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

class LogoutHandler(BS.BaseHandler):
    def get(self):
        if self.current_user is not None:
            self.session['user'] = None
        self.redirect('/')


