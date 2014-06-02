#!/usr/bin/env python


import logging as log

import facebook

import friendtube.parsers as rparse
import friendtube.querys as querys
import BaseHandler as BS

class ListHandler(BS.BaseHandler):
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

class OwnListHandler(ListHandler):
    def get(self):
        # we call the parent with other query.
        super(OwnListHandler, self).get(querys.fql_ownvideos , fql = True)

