#!/usr/bin/env python


import logging as log

import facebook

import friendtube.parsers as rparse
import friendtube.querys as querys
import BaseHandler as BS

class AdvancedListHandler(BS.BaseHandler):
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


class ListHandler(BS.BaseHandler):
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


