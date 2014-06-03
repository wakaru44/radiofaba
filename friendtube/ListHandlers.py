#!/usr/bin/env python


import logging as log

import facebook

import friendtube.parsers as rparse
import friendtube.querys as querys
import BaseHandler as BS

class ListHandler(BS.BaseHandler):
    def get(self, query = None, fql = False):
        """this get allows us to pass also a query parameter and ease
        overriding"""
        try:
            parsed_list = self.new_get_video_listing(query, fql) # NOTE we can override the query here.
            # automatic flow ENABLED
            if parsed_list["error"] == "Please relogin again":
                error = self.redirect("/logout")  # If we detect logged out here, go home
            else:
            # with the old, show sample data, this should be activated
            ### And render
                self.render(dict(
                            playlist = parsed_list["data"],
                            error = parsed_list["error"]
                        ),
                        #"player.html"
                        "player-0.2.html",
                        user = self.current_user
                        )
        except LogoutException as e:
            log.warning("Logout final catch")
            log.exception(e)
            self.redirect("/logout")
        

    def new_get_video_listing(self, query = None, fql = False):
        """new method.
        Abstracts everything related to populating a list. 
        If it cant get proper results from the outside, gather the error info
        and send also sample data.
        The Idea behind this new methods is using more map and ease method
        injection during testing
        """
        if query == None:
            log.debug("using default query")
            query = querys.filters_newsfeed  # This is the default query
            fql = True
        fblist = self.do_query(query, fql)
        # sample data failover
        if fblist["data"] == []:
            # then load the sample results
            log.warning("Loading sample results")
            import friendtube.sampleresult as smpl
            listing = rparse.parse_json_video_listing(smpl.result)
        else:
            listing = rparse.parse_json_video_listing(fblist)
        return { "data":listing, "error":fblist["error"] }

##    def get_video_listing(self, query = querys.filters_newsfeed):
##        """ gets a list of videos and returns it as a list of thingis.
##        To take a look at what kind of list and dicts we expect, take a 
##        look at the parsers.py module in friendtube
##        DEPRECATED. now we prefer do_query
##        """
##        #query = querys.filters_newsfeed
##        graph = facebook.GraphAPI(self.current_user['access_token'])
##        try:
##            log.debug("get video listing Query: " + query)
##            # Perform the fql query
##            result = graph.fql(query)
##            log.debug( u"result from get_video_listing: "+ repr(result.called))
##            video_list = rparse.parse_json_video_listing(result)
##            result_parsed = rparse.clean_list(video_list)
##            log.debug( u"result from get_video_listing: "+ repr(result))
##            # GraphAPIError , and if there is expired, means that we need to relogin
##            # GraphAPIError 606, and if there is "permission" means we have no rights
##        except Exception as e:
##            log.exception(e)
##            try:
##                # try to guess if we run out of time
##                if e.message.find(u"Session has expired") > 0 or e.message.find(u"the user logged out") > 0:
##                    #thing = u"Please go to <a href=\"/\">home</a>, logout, and come back in"
##                    log.warning("The user session expired")
##                    # and try to extend the session
##                    #TODO: it does not work this way. delete this 
##                    graph = facebook.GraphAPI(self.request.cookies)
##                    extending = graph.extend_access_token(
##                        FACEBOOK_APP_ID,
##                        FACEBOOK_APP_SECRET)
##                    result = graph.fql(query)
##                    result_parsed = rparse.parse_json_video_listing(result)
##                else:
##                    log.warning("something bad happened")
##                    raise
##            except Exception as e:
##                raise
##
##            # then load the sample results
##            import friendtube.sampleresult as smpl
##            result_parsed = rparse.parse_json_video_listing(smpl.result)
##        return result_parsed


class OwnListHandler(ListHandler):
    def get(self):
        # we call the parent with other query.
        super(OwnListHandler, self).get(querys.fql_ownvideos , fql = True)

