#!/usr/bin/env python

import logging as log
import datetime
import re

import friendtube.parse_youtube as p_y

def map_fb_to_custom(element = None):
    """map facebook's result to our personal format"""
    current = {}
    try:
        #current["link"] = get_embed(element["attachment"]["href"]) # old call
        current["link"] = get_embed(element)
    except NotImplementedError:
        current["link"] = parse_link(element)
    current["actor"] = parse_actor(element)
    current["created"] = parse_created(element)
    current["title"] = parse_title(element)
    current["desc"] = parse_description(element)
    current["preview"] = parse_preview(element)
    return current

def parse_fb_result_listing(fb_result = None):
    """ converts the result of a fb query to the expected dicts
    
    We will expect  a list of dict like this:
        [
        {
          video["link"],
          video["title"],
	  video["desc"],
	  video["preview"]
         }
         ]
    """
    return [ map_fb_to_custom(elem) for elem in fb_result["data"] ]
#    #assert(type(fb_result) == type({}))
#    plist = []  # list of videos
#    #return plist
#    for element in fb_result["data"]:
#        #inside this for you could find all the content of map_fb_to_custom.
#        plist.append(current)
#    return plist 

def parse_title(element = None):
    """getter method for the href element of the facebook results"""
    #- fall to None by default
    if element == None:
        return None

    #- get the title or none
    title = ""
    try:
        title = element["attachment"]["name"]
    except KeyError:
        return None

    return title


def parse_link(element = None):
    """getter method for the href element of the facebook results"""
    #- fall to None by default
    if element == None:
        return None

    #- get the link or none
    link = ""
    try:
        link = element["attachment"]["href"]
    except KeyError:
        return None

    return link

def parse_created(element = None):
    assert(element != None)
    created = "Disabled"
    try:
        created = datetime.datetime.fromtimestamp(int(element["created_time"])).strftime('%Y-%m-%d %H:%M')
    except KeyError as e:
        log.warning("Missing created time. we might be parsing sample data")
    except Exception as e:
        log.exception(e)
    return created


def parse_actor(element = None):
    assert(element != None)
    actor = "Disabled"
    try:
        actor = element["actor_id"]
    except KeyError as e:
        log.warning("Missing actor_id. we might be parsing sample data")
    except Exception as e:
        log.exception(e)
    return [actor]

def parse_preview(element = None):
    """tries to get a preview image for the video"""
    preview = u"/style/preview_default.png" # It will always fail back to this
    if element == None:
        return preview

    try:
        get_preview = element["attachment"]["media"][0]["src"]
        if get_preview == "":
            raise IndexError
        preview = get_preview
    except (IndexError,KeyError) as e:
        log.warning("loading video default preview picture")
        log.debug(e) # might be log.exception(e)
        log.debug("See the provided element:")
        log.debug(repr(element))
    return preview

def parse_description(element = None):
    """Tries to get the description content."""
    if element == None:
        return None

    desc = ""
    msg = ""
    try:
        desc = element["attachment"]["description"]
        msg = element["message"]
    except KeyError:
        return None

    return u"{0}\n<br />\n ---------------------<br /> {1}".format(
                            shorten_comment(desc),
                            shorten_comment(msg)
                            )


def get_embed(fb_elem = None):
    """
    Receives a facebook result element.
    returns the embed link to the video provided
    If no element, or wrong, returns None
    """
    #- pre-flight checks
    link = ""
    try:
        if (fb_elem == None) or (fb_elem == ""):
            raise KeyError("Element not properly provided")

        if type(fb_elem) == type(""):
            log.warning("get embed falling back to legacy. please update the code")
            link = fb_elem
        else:
            link = fb_elem["attachment"]["href"]
    except KeyError as e:
        return None

    #- then proceed
    flink = "" # resulting link
    if link.find("youtu") > 0:
        # it is probably a youtube video
        flink = p_y.get_embed_youtube(link)
    elif link.find("vimeo") > 0:
        # Its probably a vimeo Video
        raise NotImplementedError, "We are still working on new video providers"
    else:
        raise NotImplementedError( "We are still working on " + link.__str__() )

    return flink


def shorten_comment(comment = None, limit = 100):
    """ makes a comment shorter than limit"""
    assert(comment != None)
    if len(comment) > limit:
        return comment[0:limit] + u"<span class=\"greyed\">... For more check your timeline</span>"
    else:
        return comment 

def clean_list(posts):
    """takes a list of videos (already parsed) and returns it clean with 
    the actors summed up in one single  list"""
    # NOT WORKING
    #TODO: implement this asap
    cleaned = []
    while len(posts) > 0 :
        elem = posts.pop()
        found = []
        #print "lookihng for: " + elem["link"]
        #print "with actor: " + repr(elem["actor"])
        indexes = range(0,len(posts))
        #for i in range(0,len(posts)):
        while len(indexes) > 0:
            i = indexes.pop()
            other = posts[i]
            #print "compared with " + other["link"]
            if elem["link"] in other["link"]:
                #print "found: " + repr(other["link"])
                #print "with actor: " + repr(other["actor"])
                found.extend(other["actor"])
                posts.pop(i)
        if len(found) == 0:
            #print "is not dupe"
            cleaned.append(elem)
        else:
            # is duplicated so add the actors
            elem["actor"].extend(found)
            #print "all: " + repr(elem["actor"])
            cleaned.append(elem)

    return cleaned

