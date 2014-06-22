#!/usr/bin/env python

import logging as log
import datetime
import re


def legacy_check(link = None):
    """returns a chopped link if given a string.
    This is because i used to pass strings, but im thinkng in
    passing list"""
    if type(link) == type(""):
        # If we are given a string, we split it ourselves
        return link.split("/")
    else:
        return link


def regex_video_id(param):
    """ try to find the regex in the string given
    """
    miregex = '(.*)v=(.*)&?(.*)'
    vid = None
    #log.debug("get video id: " + repr(param))
    try:
        rs = re.search(miregex, param)
        params = rs.group(2)
        #log.debug("params " + params)
        vid = params
        #id = params.split("&")[0] if params != None and len(params)>12 else params
    except Exception as e:
        #log.debug("HURU")
        #log.exception(e)
        pass # yes, we pass
    return vid

def search_video_id(broken_link):
    """try to find the gold in the link
    regular links can be inverted too. so we search the whole list
    """
    for param in broken_link:
        vid = regex_video_id(param)
        if vid:
            return vid

def get_id_regular_link(link = None):
    """return the id for a giver regular link. 
    no shortlink, no attribution, no...
    """
    #Legacy compatibility
    choppedLink = legacy_check(link)
    # dont bother if we are none.
    if link == None:
        return link

    vid_url_params = choppedLink[3].split("&")
    # Search the id in the list of elements of the url
    vid = search_video_id(vid_url_params)

    # And dont forget the links with hashtags #
    vid = vid.split("#")[0]

    return vid # change this var names TODO


def get_id_attribution(link = None):
    """ Return the id of a youtube video for a given link with attribution
    params"""
    log.debug("attribution link: " + repr(link))
    choppedLink = legacy_check(link)
    id = None
    try:
        # First try to get the relevant part, that is encoded
        step1 = choppedLink[3][choppedLink[3].find("watch"):]
        # Then stplit the other encoded params
        step2 = step1[12:].split("%")
        # and get the good part
        step3 = step2[0]
        id = step3  # choppedLink[3][choppedLink[3].find("watch"):][12:].split("%")[0]
    except Exception as e:
        raise  e # dont care 'bout issues here. all will be NotImplementedError 

    # If we havent found a match, then this is not implemented.
    if id == "":
        raise Exception("no recognised kind of link")

    return id

def get_id_shortlink(link = None):
    """
    Returns the id for a given shortlink.
    defaults to none
    """
    choppedLink = legacy_check(link)
    id = None
    try:
        id = choppedLink[3]  # or -1 instead of 3
    except:
        pass #dont care bout issues here
    return id


def compose_embed_youtube(video_id = None):
    """return a link to youtube"""
    assert(video_id != None)
    return "https://www.youtube.com/embed/{0}?enablejsapi=1&wmode=opaque".format(
                video_id
                )


def get_embed_youtube(link = None):
    """
    Returns the embed link to the video provided.
    This is thinking only in youtube"""
    assert(link != None)
    assert(link != "")
    log.debug( "preparsed link: " + link)
    video_id = ""
    try:
        # break the link
        choppedLink = link.split("/")
        if choppedLink[2].find("youtu.be") >= 0:
            # Parse short link getting only last piece
            video_id = get_id_shortlink(choppedLink)
        elif choppedLink[3].find("attribution_link") >= 0 :
            # Its an attribution link, a bit special
            video_id = get_id_attribution(choppedLink)
        else:
            # This should be a regular link
            video_id = get_id_regular_link(choppedLink)

        # and finally compose the embed link
        flink = compose_embed_youtube(video_id)
        log.debug( "compound link: " + flink)
    except Exception as e:
        log.error("Something weird happened when ending getting embed youtube")
        log.exception(e)
        raise NotImplementedError( "We are still working on links like " + link)

    return flink

