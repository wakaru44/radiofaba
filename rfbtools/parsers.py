#!/usr/bin/env python

import logging as log

def parse_json_video_listing(fb_result = None):
    """ converts the result of a fb query to the expected dicts
    
    We are expecting a list of dict like this:
        [
        {
          video["link"]"
          video["title"] 
	  video["desc"]
	  video["preview"]
         }
         ]
     """
    #assert(fb_result != None)
    plist = []  # list of videos
    # TODO: do some parsing matey
    #return plist
    for element in fb_result["data"]:
        #log.debug("element"+ repr(element))
        current = {}
        #current["link"] = element["attachment"]["href"]
        current["link"] = get_embed(element["attachment"]["href"])
        current["title"] = element["attachment"]["name"]
        current["desc"] = u"{0}\n<br />\n ---------------------<br /> {1}".format(
                            shorten_comment(element["attachment"]["description"]),
                            shorten_comment(element["message"])
                            )
        current["preview"] = element["attachment"]["media"][0]["src"]

        plist.append(current)
    #return [fb_result]  # TODO: by now, for debug, we provide the full list
    return plist  # TODO: by now, for debug, we provide the full list


def get_embed_youtube(link = None):
    """Returns the embed link to the video provided.
    This is the new method, thinking only in youtube"""
    assert(link != None)
    assert(link != "")
    flink = "http://www.youtube.com/embed/{0}?enablejsapi=1&wmode=opaque".format(
        link.split("/")[-1].split("&")[0].split("?")[1][2:]
    )
    log.debug( "compound link"+ flink)
    return flink


def get_embed(link = None):
    """returns the embed link to the video provided
    """
    # TODO: a good idea to do this, is just split by / and return the last part
    rlink = "" # resulting link
    assert(link != None)
    assert(link != "")
    if link.startswith("http://youtu.be/"):
        ## Parse short link
        rlink = link[16:]
    elif link.startswith("http://www.youtube.com/"):
        ## Parse long link
        rlink = link[31:]
    elif link.startswith("https://www.youtube.com/"):
        ## Parse long link
        rlink = link[32:]
    else:
        rlink = link
        #raise ValueError("crap. new kind of link")

    flink = "http://www.youtube.com/embed/{0}?enablejsapi=1&wmode=opaque".format(
                     trim_youtube_video(rlink))
    log.debug( "compound link"+ flink)
    return flink

def trim_youtube_video( link_end = None):
    """ gets the last part of a youtube url and returns only the video id """
    assert(link_end != None)
    return link_end.split("?")[0]
    

def shorten_comment(comment = None, limit = 100):
    """ makes a comment shorter than limit"""
    assert(comment != None)
    if len(comment) > limit:
        return comment[0:limit] + u"<span class=\"greyed\">... For more check your timeline</span>"
    else:
        return comment 
