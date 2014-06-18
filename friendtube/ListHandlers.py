#!/usr/bin/env python


import logging as log

import facebook

import friendtube.parsers as rparse
import friendtube.querys as querys
import BaseHandler as BS
from BaseHandler import LogoutException

player_template = "player-0.2b.html"

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
                        player_template,
                        user = self.current_user
                        )
        except LogoutException as e:
            log.warning("Logout final catch")
            log.exception(e)
            self.redirect("/logout")
        

    def new_get_video_listing(self, query = None, fql = False, user = None):
        """new method.
        Abstracts everything related to populating a list. 
        If it cant get proper results from the outside, gather the error info
        and send also sample data.
        The Idea behind this new methods is using more map and ease method
        injection during testing
        """
        if user == None:
            user = self.current_user
        if query == None:
            log.debug("using default query")
            query = querys.filters_newsfeed  # This is the default query
            fql = True
        fblist = self.do_query(query, fql, user)
        if fblist["data"] == []:
            # sample data failover flow
            # load the sample results
            log.warning("Loading sample results")
            import friendtube.sampleresult as smpl
            listing = rparse.parse_json_video_listing(smpl.result_works)
        else:
            # we clean the data received.
            raw_listing = rparse.parse_json_video_listing(fblist)
            listing = rparse.clean_list(raw_listing)
            # In the next version, we will use 
            # new_translate_fbresult_to_listing(fb_result)
            # with no ordering required
        return { "data":listing, "error":fblist["error"] }


class OwnListHandler(ListHandler):
    def get(self):
        # we call the parent with other query.
        super(OwnListHandler, self).get(querys.fql_ownvideos , fql = True)

