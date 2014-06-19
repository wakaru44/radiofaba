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
            parsed_list = self.get_video_listing(query, fql) # NOTE we can override the query here.
            # automatic flow ENABLED
            if parsed_list["error"] == "Please relogin again":
                log.warning("Self redirecting to logout")
                error = self.redirect("/logout")  # If we detect logged out here, go home
            else:
            # with the old, show sample data, this should be activated
            ### And render
                log.debug("Rendering List")
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
        

    def get_video_listing(self, query = None, fql = False, user = None):
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
        listing = []  # we need at least the default empty listing
        if fblist["data"] == []:
            # sample data failover flow
            # load the sample results
            #DEPRECATED but i will keep the code
            #log.warning("Loading sample results")
            #import friendtube.sampleresult as smpl
            #listing = rparse.parse_fb_result_listing(smpl.result_works)
            pass # read above comments to clarify
        else:
            # we clean the data received.
            log.debug("cleaning the data received from fb")
            raw_listing = rparse.parse_fb_result_listing(fblist)
            listing = rparse.clean_list(raw_listing)
            log.debug("clean res: " + repr(listing))
        return { "data":listing, "error":fblist["error"] }


class OwnListHandler(ListHandler):
    def get(self):
        # we call the parent with a query about our own shared videos.
        super(OwnListHandler, self).get(querys.fql_ownvideos , fql = True)


class OtherListHandler(ListHandler):
    def get(self):
        # we call the parent with other query.
        #super(OtherListHandler, self).get(querys.fql_from_specific_list_of_friends , fql = True) #fql style
        #super(OtherListHandler, self).get(querys.fql_from_dorota_and_list_of_friends , fql = True) #fql style
        super(OtherListHandler, self).get(querys.fql_from_dorota_and_vetusta , fql = True) #fql style
        #super(OtherListHandler, self).get(querys.fql_from_good_fellas , fql = True) #fql style


class FromAFriendHandler(ListHandler):
    def get(self):
        """Shows the list of videos from a specific friend.
        """
        #TODO this is quite dangerous in a production app....
        # but for now, seems useful...
        try:
            friend = self.request.params["friend"]
            if friend.isdigit():
                # then we consider the friend as valid and go to fb
                friend_query = querys.fql_from_list_of_friends.format('"' + friend + '"')
                log.debug(friend_query)
                super(FromAFriendHandler, self).get(friend_query , fql = True) #fql style
            else:
                self.render({"data": "What exactly are you looking for?"})
        except Exception as e:
            log.warning("pokemon exception")
            log.exception(e)
 
class MultiQueryListHandler(ListHandler):
    """uses a multifql custom method.
    the multiquerys are isued as json encoded querys, with the fql flag on.
    It can me hand made, or can be formed with the querys.compose_multi method.
    """
    #TODO we still need to handle the multiple results to be able to do
    #something with this.
    def get(self):
        from mock import patch
        with patch("friendtube.parsers.clean_list", lambda x: x):
            # we have to patch the clean_list to avoid failures
            #super(MultiQueryListHandler, self).get(querys.fql_multi_query_fbexample, #hand made
            #super(MultiQueryListHandler, self).get(querys.fql_multi_query_composed, # auto composed
            super(MultiQueryListHandler, self).get(querys.fql_multi_query2, # trying an old query
                                               fql = True)


        log.debug("HIIIIII are we really hitting this somehow?")
        self.render()

class ListHandlerWithFriends(ListHandler):
    """Shows a regular player with a list of clickable friends with more content
    """
    #TODO we still need to handle the multiple results to be able to do
    #something with this.
    def get(self):
        from mock import patch
        with patch("friendtube.parsers.clean_list", lambda x: x):
            # we have to patch the clean_list to avoid failures
            myQuery = [querys.fql_list_of_good_source_friends,
                       querys.filters_newsfeed
            ]
            super(ListHandlerWithFriends, self).get(querys.fql_multi_query2, # trying an old query
                                               fql = True)



class PatchedListHandler(ListHandler):
    """this class is an example of how to offer modified results with patched
    methods.
    """
    def get(self):
        # we call the parent with other query.
        #super(OtherListHandler, self).get(querys.fql_ownvideos , fql = True) #fql style
        #super(OtherListHandler, self).get(querys.filters_based01 , fql = True)

        #super(OtherListHandler, self).get(querys.fql_friends_on_newsfeed, fql = True) # fails to clean_list
        # To avoid the errors cleaning the list, due to the empty pieces in the
        # result, we patch the clean_list method.
        from mock import patch
        with patch("friendtube.parsers.clean_list", lambda x: x):
            super(OtherListHandler, self).get(querys.fql_friends_on_newsfeed, fql = True)

