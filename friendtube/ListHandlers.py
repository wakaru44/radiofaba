#!/usr/bin/env python


import logging as log

import facebook

import friendtube.parsers as rparse
import friendtube.querys as querys
import BaseHandler as BS
from BaseHandler import LogoutException

player_template = "player-0.2b.html"
with_friends_template = "player_withfriends-0.2.html"
friends_template = "player_friend-0.2.html"
future_template = "player-0.2c.html"
mobile_template ="player_mobile-0.2a.html"
fbvideo_template ="player_facebook-0.1.html"

class ListHandler(BS.BaseHandler):
    def get(self, query = None, fql = False, template = player_template ):
        """this get allows us to pass also a query parameter and ease
        overriding"""
        try:
            parsed_list = self.get_video_listing(query, fql) # NOTE we can override the query here.
            # automatic flow ENABLED
            if parsed_list["error"] == "Please relogin again":
                raise LogoutException("The user must login again")
                #log.warning("Self redirecting to logout")
                #error = self.redirect("/logout")  # If we detect logged out here, go home
            else:
            # with the old, show sample data, this should be activated
            ### And render
                log.debug("Rendering List")
                self.render(dict(
                            playlist = parsed_list["data"],
                            error = parsed_list["error"]
                        ),
                        #"player.html"
                        template,
                        user = self.current_user
                        )
        except LogoutException as e:
            log.warning("Logout final catch. Redirecting")
            log.warning(e)
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
        video_list_clean = []  # we need at least the default empty listing
        if fblist["data"] == []:
            # sample data failover flow
            # load the sample results
            #DEPRECATED but i will keep the code
            #log.warning("Loading sample results")
            #import friendtube.sampleresult as smpl
            #video_list_clean = rparse.parse_fb_result_listing(smpl.result_works)
            pass # read above comments to clarify
        else:
            # we clean the data received.
            log.debug("cleaning the data received from fb")
            video_list_parsed = rparse.parse_fb_result_listing(fblist)
            video_list_clean = rparse.clean_list(video_list_parsed)
            # log.debug("clean res: " + repr(video_list_clean)) #noisy
        return { "data":video_list_clean, "error":fblist["error"] }


class FutureListHandler(ListHandler):
    def get(self):
        from mock import patch
        #with patch("friendtube.parsers.clean_list", lambda x: x):
        with patch("friendtube.parsers.shorten_comment", lambda x: x):
            super(FutureListHandler, self).get(querys.filters_newsfeed,
                                              fql = True,
                                              template = future_template)


class MobileListHandler(ListHandler):
    def get(self):
        #super(MobileListHandler, self).get(template=mobile_template)
        padre = super(MobileListHandler, self)
        log.debug("padre: " + repr(dir(padre)))
        geto = padre.get(template=mobile_template)


class FbVideoListHandler(ListHandler):
    def get(self):
        #super(MobileListHandler, self).get(template=mobile_template)
        padre = super(FbVideoListHandler, self)
        geto = padre.get(querys.fql_fbvideos_from_newsfeed,
                         fql = True,
                         template=fbvideo_template)


class OwnListHandler(ListHandler):
    def get(self):
        # we call the parent with a query about our own shared videos.
        super(OwnListHandler, self).get(querys.fql_ownvideos , fql = True)


class OtherListHandler(ListHandler):
    def get(self):
        # we call the parent with other query.
        #super(OtherListHandler, self).get(querys.fql_from_specific_list_of_friends , fql = True) #fql style
        #super(OtherListHandler, self).get(querys.fql_from_dorota_and_list_of_friends , fql = True) #fql style
        super(OtherListHandler, self).get(querys.fql_videos_from_friends_on_newsfeed , fql = True) #fql style
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
                super(FromAFriendHandler, self).get(friend_query,
                                                    fql = True,
                                                    template = friends_template) #fql style
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
    def get(self):
        """
        Second Attempt to use multi query.
        Here we just take some query, get the data from it, and pass the parsed
        results to the template.
        The heavy-lifting of querying fb and processing the results is done in
        other methods.
        """
        #TODO: writting this
        try:
            # Multquery definition
            log.info("Showing latest videos and panel of friends")
            query = querys.compose_multiquery([
                        querys.filters_newsfeed,
                        querys.fql_friends_profiles.format(querys.fql_list_of_good_source_friends_and_others) # few but somehow good results
                        #querys.fql_friends_profiles.format(querys.fql_friends) # too few results
                        #querys.fql_friends_profiles.format(querys.fql_friends_on_newsfeed)  # too many irrelevant results
            ])
            parsed_results = self.get_video_and_friends_listing(query, fql=True) # NOTE we can override the query here.
            #log.debug("parsed results: " + repr(parsed_results)) # noisy

            # automatic flow ENABLED
            if parsed_results["error"] == "Please relogin again":
                raise LogoutException("The user must login again")
            elif parsed_results["error"] != "":
                # there was an error, so we will render only that
                log.error("detected" + parsed_results["error"])
                self.render(dict(
                        playlist = None, data = None,
                        error = parsed_results["error"]
                    ),
                    with_friends_template,
                    user = self.current_user
                )
            else:
                # And if all good, render
                log.debug("Rendering List")
                self.render(dict(
                            playlist = parsed_results["data"][0]["payload"],
                            friends = parsed_results["data"][1]["payload"],
                            #data = parsed_results["data"][1],
                            error = parsed_results["error"]
                        ),
                        #"player.html"
                        with_friends_template,
                        user = self.current_user
                        )
        except LogoutException as e:
            log.warning("Logout final catch. Redirecting")
            log.warning(e)
            self.redirect("/logout")
        

    def get_video_and_friends_listing(self, query = None, fql = False, user = None):
        """
        custom method to handle multi query
        """
        if user == None:
            user = self.current_user
        if query == None:
            log.error("no default query") # multi query is a little bit more strict that the single
            raise NotImplemented("Contact the developer. No default query configured.")

        fbresults = self.do_query(query, fql, user)

        querys_results = []  # Default to empty
        if fbresults["data"] != []:
            # we have to adapt the data received.
            log.debug("cleaning the data received from fb")
            for query in fbresults["data"]:
                qname = query["name"]
                qresult = query["fql_result_set"]
                if qname == "query1":
                    #- selecting specific querys through name
                    video_list_parsed = rparse.parse_fb_result_listing({"data": qresult}) # gets the listing in our format and structure
                    #listing = rparse.clean_list(video_list_parsed)  # eliminate duplicates
                    #log.debug("clean res: " + repr(video_list_parsed)) #noisy
                    querys_results.append({ "name": qname,  
                                     "payload": video_list_parsed})
                else:
                    #- the default behaviour for unnamed querys
                    querys_results.append({"name": qname,
                                             "payload": qresult})

        return { "data":querys_results, "error":fbresults["error"] }


    #def get(self):
    #    from mock import patch
    #    with patch("friendtube.parsers.clean_list", lambda x: x):
    #        # we have to patch the clean_list to avoid failures
    #        myQuery = [querys.fql_list_of_good_source_friends,
    #                   querys.filters_newsfeed
    #        ]
    #        super(ListHandlerWithFriends, self).get(querys.fql_multi_query2, # trying an old query
    #                                           fql = True)



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

