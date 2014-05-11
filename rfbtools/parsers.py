#!/usr/bin/env python

import logging as log

def parse_json_video_listing(fb_result = None):
    """ converts the result of a fb query to the expected dicts
    
    We will expect  a list of dict like this:
        [
        {
          video["link"]"
          video["title"] 
	  video["desc"]
	  video["preview"]
         }
         ]
     """
    plist = []  # list of videos
    #return plist
    for element in fb_result["data"]:
        current = {}
        current["link"] = get_embed(element["attachment"]["href"])
        current["title"] = element["attachment"]["name"]
        current["desc"] = u"{0}\n<br />\n ---------------------<br /> {1}".format(
                            shorten_comment(element["attachment"]["description"]),
                            shorten_comment(element["message"])
                            )
        current["preview"] = element["attachment"]["media"][0]["src"]

        plist.append(current)
    return plist 


def get_embed_youtube(link = None):
    """Returns the embed link to the video provided.
    This is the new method, thinking only in youtube"""
    assert(link != None)
    assert(link != "")
    rlink = ""
    if link.find("youtu.be") > 0:
        ## Parse short link, as it is a little bit special,use only last piece
        rlink = link.split("/")[-1]
    elif link.find("attribution_link") > 0 :
        ## Its an attribution link, so im not sure how to handle it yet
        #TODO: research this kind of link and how to parse it better.
        rlink = link.split("://")[1][64:].split("%")[0]
    else:
        rlink = link.split("/")[-1].split("&")[0].split("?")[1][2:]
    # There are also some links to youtube that have # and params.
    rlink = rlink.split("#")[0]
    # and then we compose our embed link
    flink = "http://www.youtube.com/embed/{0}?enablejsapi=1&wmode=opaque".format(
            rlink
    )
    return flink


def get_embed(link = None):
    """returns the embed link to the video provided
    """
    flink = "" # resulting link
    assert(link != None)
    assert(link != "")
    log.debug( "preparsed link: " + link)
    if link.find("youtu") > 0:
        # it is probably a youtube video
        flink = get_embed_youtube(link)
    elif link.find("vimeo") > 0:
        # Its probably a vimeo Video
        raise NotImplementedError, "We are still working on new video providers"
    else:
        raise NotImplementedError, "We are still working on " + link.__str__()

    log.debug( "compound link: " + flink)
    return flink


def shorten_comment(comment = None, limit = 100):
    """ makes a comment shorter than limit"""
    assert(comment != None)
    if len(comment) > limit:
        return comment[0:limit] + u"<span class=\"greyed\">... For more check your timeline</span>"
    else:
        return comment 

def nice_exception( exception = None, html = False ):
    """This paints an exception as an formated string
    html formatting NOTIMPLEMENTED
    by now its a pityfull method.
    TODO: Take real information from exceptions, then format it"""
    if not exception:
        return "This is not the exception you are looking for"
    import sys
    return repr(sys.exc_info())



