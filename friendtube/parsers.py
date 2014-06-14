#!/usr/bin/env python

import logging as log
import datetime

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
    #assert(type(fb_result) == type({}))
    plist = []  # list of videos
    #return plist
    for element in fb_result["data"]:
        current = {}
        try:
            current["link"] = get_embed(element["attachment"]["href"])
        except NotImplementedError:
            current["link"] = element["attachment"]["href"]
        current["actor"] = parse_actor(element)
        current["created"] = parse_created(element)
        current["title"] = element["attachment"]["name"]
        current["desc"] = parse_description(element)
        current["preview"] = parse_preview(element)

        plist.append(current)
    return plist 

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
    assert(element != None)
    preview = u"/style/preview_default.png" # It will always fail back to empty.
    # TODO: find default image
    try:
        get_preview = element["attachment"]["media"][0]["src"]
        if get_preview == "":
            raise IndexError
        preview = get_preview
    except IndexError as e:
        log.warning("A preview image was expected")
        log.exception(e)
        log.warning("See the provided element:")
        log.warning(repr(element))
    return preview

def parse_description(element = None):
    """Tries to get the description content."""
    assert(element != None)
    return u"{0}\n<br />\n ---------------------<br /> {1}".format(
                            shorten_comment(element["attachment"]["description"]),
                            shorten_comment(element["message"])
                            )


def get_embed_youtube(link = None):
    """Improved version. 
    Returns the embed link to the video provided.
    This is the new method, thinking only in youtube"""
    assert(link != None)
    assert(link != "")
    log.debug( "preparsed link: " + link)
    rlink = ""
    try:
        # break the link
        blink = link.split("/")
        if blink[2].find("youtu.be") >= 0:
            # Parse short link getting only last piece
            rlink = blink[-1]
        elif blink[3].find("attribution_link") >= 0 :
            # Its an attribution link, a bit special
            rlink = blink[3][blink[3].find("watch"):][12:].split("%")[0]
        else:
            # This should be a regular link
            #rlink = blink[3].split("&")[0].split("?")[1][2:]
            rlink = blink[3].split("&")
            log.debug("HERE: " + repr(rlink))
            # But regular links can be inverted too.
            ######################
            # fancy (and not very readable) way to clean a list of youtube
            # videos
            # l = list_of_youtube_videos
            # miregex = '(.*)v=(.*)&?(.*)'
            # map(lambda x: x.split("&")[0] if x != None and (len(x) > 12) else x ,
            #     map(lambda x:  x.group(2) if x else None, 
            #         map(lambda x: re.search(miregex, x), l)
            #        )
            #    )
    except Exception as e:
        log.error("Something weird happened when trying to get embed link")
        log.exception(e)
        raise NotImplementedError( "We are still working on links like " + link)
    # and dont forget those links with # params
    try: 
        #TODO: this part causes many issues and false positives. improve.
        rlink = rlink.split("#")[0]
        # and finally compose the embed link
        flink = "http://www.youtube.com/embed/{0}?enablejsapi=1&wmode=opaque".format(
                rlink
                )
        log.debug( "compound link: " + flink)
    except Exception as e:
        log.error("Something weird happened when ending getting embed youtube")
        log.exception(e)
        raise NotImplementedError( "We are still working on links like " + link)
    return flink


def get_embed(link = None):
    """returns the embed link to the video provided
    """
    flink = "" # resulting link
    assert(link != None)
    assert(link != "")
    if link.find("youtu") > 0:
        # it is probably a youtube video
        flink = get_embed_youtube(link)
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

