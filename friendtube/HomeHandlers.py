#!/usr/bin/env python

import logging as log

import facebook

import friendtube.parsers as rparse # the dep on this is minimal
import friendtube.querys as querys
import BaseHandler as BS
from BaseHandler import LogoutException



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
            friends["error"] = "Log in with your facebook id"
            current_user = None
            # we should show the demo page anyway
        self.render({"friends" : friends["data"], "error":friends["error"] },
                    "home-0.2.html",
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

    def post(self, template = "home.html"):
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


class CanvasHandler(HomeHandler):
    def get(self):
        self.render({"data" : repr(self.request.params), "error":"errorerror" },
                    "canvas.html",
                    user = self.current_user)


    def post(self):
        """handles the login process differently than HomeHandler, triggering it async"""
        log.debug("PARSING POST")
        log.debug(dir(super(HomeHandler)))
        log.debug(super(HomeHandler))
        self.render({"data":self.request.params}, "canvas.html", user = self.current_user)

class LogoutHandler(BS.BaseHandler):
    def get(self):
        try:
            if self.current_user is not None:
                self.session['user'] = None
        except LogoutException:
            pass  # expected
        self.redirect('/')


class TestHandler(BS.BaseHandler):
    def get(self):
        data = ""
        data += "<h2>{0}</h2>".format("dir(self.app)")
        data += self.list2html(dir(self.app))
        data += "<h2>{0}</h2>".format("active instance request application_url") 
        data += self.thing2html(self.app.active_instance.request.application_url)
        data += "<h2>{0}</h2>".format("app config")
        data += self.thing2html(self.app.config)
        data += "<h2>{0}</h2>".format("app config")
        data += self.thing2html(self.app.config)
        self.render(values = {"data": data},
                    template = "home-0.2.html",
                    user = self.current_user)

    def list2html(self, things = None, htmlid = None, htmlclass = None):
        """takes a list and returns an html string"""
        html = u""
        if things == None:
            return html
        else:
            idout = u" id=\"{0}\" ".format(htmlid) if htmlid else ""
            classout = u" class=\"{0}\" ".format(htmlclass) if htmlclass else ""
            html += u"<ul{0}{1}>\n".format(idout, classout)
            for thing in things:
                element = u"<li>{0}</li>\n".format(thing)
                html += element
            html += u"</ul>\n"
            return html

    def thing2html(self, thing):
        """creates a p  element from something"""
        html_escape_table = {
                    "&": "&amp;",
                    '"': "&quot;",
                    "'": "&apos;",
                    ">": "&gt;",
                    "<": "&lt;",
                    }
        what = repr((thing)).__str__()
        flatting = "".join(c for c in what) # things works somehow fucki
        html_escaped = "".join(html_escape_table.get(c,c) for c in flatting)
        return "<pre>{0}</pre>\n".format(html_escaped)


        


