#!/usr/bin/env python

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
        print("DEBUG:","element", repr(element))
        current = {}
        #current["link"] = element["attachment"]["href"]
        current["link"] = get_embed(element["attachment"]["href"])
        current["title"] = element["attachment"]["name"]
        current["desc"] = element["attachment"]["description"] + "\n<br />\n" +   element["message"]
        current["preview"] = element["attachment"]["icon"]

        plist.append(current)
    #return [fb_result]  # TODO: by now, for debug, we provide the full list
    return plist  # TODO: by now, for debug, we provide the full list


def get_embed(link = None):
    """returns the embed link to the video provided
    """
    rlink = "" # resulting link
    assert(link != None)
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

    flink = "http://www.youtube.com/embed/{0}?enablejsapi=1&wmode=opaque".format(rlink)
    print("DEBUG:", "compound link", flink)
    return flink
