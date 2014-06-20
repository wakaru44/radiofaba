#!/usr/bin/env python
################################################################################
#    List of queryes for easy retrieval
################################################################################

################################################################################
#   Get friends querys
################################################################################
# with the v1 it returned all your friends
# with the v2 only returns your friends that are also using this same app, and
# have signed dunno how (but my uncle is using it and does not appear as friend)
fql_friends = """ SELECT uid2
                FROM friend
                WHERE uid1 == me()
"""

fql_friends_profiles = """SELECT
name, id, pic
FROM profile
WHERE id in ({0})
"""

# Get the friends that also use the app, and its pictures
graph_friends = "me/friends?fields=name,id,picture"

# Get the list of friends (not only the ones that use the app)
# With the api v2, it only gets aliases, not real uid
graph_friends_nonapp = "me/taggable_friends"

# Get the friends that have shared something in the newsfeed
# (that is, the friends that are lately active)
fql_friends_on_newsfeed = """ SELECT 
    actor_id
FROM stream
WHERE filter_key in ( 
    Select filter_key
        from stream_filter
        where uid = me() 
        AND type in ('newsfeed')
    )
AND
    strpos(attachment.href, "youtu") >= 0
LIMIT 10000
"""

# get the pic of a friend. REQUIRES a parameter
graph_pic = "{facebookId}/picture?type=square"

################################################################################
#   Get videos querys
################################################################################
# old query to get the results of your. better results with the 1.0 api. almost
# nothing with 2.0 api.
friends_based = """ SELECT
            message,
            actor_id,
            created_time,
            attachment.href,
            attachment.name,
            attachment.description,
            attachment.media.src
        FROM stream
        WHERE source_id in
            (SELECT uid2
                FROM friend
                WHERE uid1 == me()
            ) 
            and
            strpos(attachment.href, "youtu") >= 0
        LIMIT 10000
        """

#Experimental. not working well by now
fql_videos_from_friends_on_newsfeed = """SELECT
            message,
            actor_id,
            created_time,
            attachment.href,
            attachment.name,
            attachment.description,
            attachment.media.src
        FROM stream
        WHERE source_id in
            (
                SELECT 
                    actor_id
                FROM stream
                WHERE filter_key in ( 
                    Select filter_key
                        from stream_filter
                        where uid = me() 
                        AND type in ('newsfeed')
                    )
                AND
                    strpos(attachment.href, "youtu") >= 0
                LIMIT 10000
            ) 
        AND
            strpos(attachment.href, "youtu") >= 0
        LIMIT 10000
"""


#Experimental. not working well by now
# takes all the videos from a specific list of friends
list_of_friends = """
               "520468721409943",
               "342714211268",
               "838894906138604",
               "12500217831",
               "10203656285228486",
               "788799174464444",
               "10203181079664632",
               "10204094479910261",
               "10203087889496668"
"""

# other_friend = """ "10203087889496668" """ # random friend
#other_friend = """ "342714211268" """ # friendly friend (minimo esf.)
vetusta = """ "12500217831" """ # friendly friend (vetusta)
other_friend = """ "12500217831" """ # friendly friend (vetusta)

dorota = """
"100000307053246"
"""

friends_with_good_results = """
"342714211268", 
"100000307053246",
"12500217831"
"""

fql_from_list_of_friends = """ SELECT
    message,
    actor_id,
    created_time,
    attachment.href,
    attachment.name,
    attachment.description,
    attachment.media.src
FROM stream
WHERE source_id in
    (
{0}
    )
AND
    strpos(attachment.href, "youtu") >= 0
LIMIT 10000
"""

fql_list_of_good_source_friends = """SELECT
            actor_id
        FROM stream
        WHERE source_id in
            (
                SELECT 
                    actor_id
                FROM stream
                WHERE filter_key in ( 
                    Select filter_key
                        from stream_filter
                        where uid = me() 
                        AND type in ('newsfeed')
                    )
                AND
                    strpos(attachment.href, 'youtu') >= 0
                LIMIT 100
            ) 
        AND
            strpos(attachment.href, 'youtu') >= 0
        LIMIT 1000000
"""
fql_from_dorota = fql_from_list_of_friends.format(dorota) # plenty results
fql_from_other_friend = fql_from_list_of_friends.format(other_friend) # no results
fql_from_specific_list_of_friends = fql_from_list_of_friends.format(list_of_friends) # few results
fql_from_dorota_and_list_of_friends = fql_from_list_of_friends.format(list_of_friends + "," + dorota) # few results (only one from dorota)
fql_from_dorota_and_vetusta = fql_from_list_of_friends.format(vetusta + "," + dorota) # 2 results (one from each)
fql_from_good_fellas = fql_from_list_of_friends.format(friends_with_good_results) # few results (only one from dorota)
# it seems that when we ask about too many friends, the results of the videos
# decrease dramatically from dozens to 1 or 3.
# but when we gather only a user that is friend, results are plenty
# if than friend (or page) is sharing videos publicly. So no videos from
# friends, like the old times so far...


# This query seems to retrieve a lot of duplicates
# And doesn't seem to get more results than the plain nf
filters_based01 = """ SELECT 
            message,
            actor_id,
            created_time,
            attachment.href,
            attachment.name,
            attachment.description,
            attachment.media.src
FROM stream
WHERE filter_key in ( 
Select filter_key
    from stream_filter
    where uid = me() 
    AND type in ('newsfeed','friendlist')
)
and strpos(attachment.href,"youtu") >= 0
LIMIT 5000
"""

########################################
#   Working Querys
########################################
# This one gets the newsfeed only from fql.
# By not this is the DEFAULT
filters_newsfeed = """SELECT 
    message,
    actor_id,
    created_time,
    attachment.href,
    attachment.name,
    attachment.description,
    attachment.media.src
FROM stream
WHERE filter_key in ( 
Select filter_key
    from stream_filter
    where uid = me() 
    AND type in ('newsfeed')
)
and strpos(attachment.href,'youtu') >= 0
LIMIT 10000
"""

# This one gets the videos of the user
fql_ownvideos = """SELECT 
    message,
    actor_id,
    created_time,
    attachment.href,
    attachment.name,
    attachment.description, 
    attachment.media.src
FROM stream 
WHERE source_id = me() 
  AND strpos(attachment.href,"youtu") >= 0
LIMIT 1000
"""

# This is a litte bit more restricted, with actor_id also
fql_ownvideos_rest = """ SELECT 
    message,
    actor_id,
    created_time,
    attachment.href,
    attachment.name,
    attachment.description, 
    attachment.media.src
FROM stream 
WHERE source_id = me() 
  AND actor_id = me()
  AND strpos(attachment.href,"youtu") >= 0
LIMIT 1000
"""


########################################
#   Multi Querys
########################################
def compose_multiquery (querys = None):
    """return a json string with the querys
    """
    assert(querys != None)
    json_query = "{"
    qnum = 1
    #- we have to remove newlines to avoid sintax issues.
    nonuline_querys = map(lambda x: " ".join(x.split("\n")), querys)
    # and replace multispaces by single spaces
    nospaced_querys = map(lambda x: " ".join(x.split()), querys)
    for query in nospaced_querys:
        #json_query = json_query + """query""" + str(qnum) + """":" """ + query + """","""
        json_query = """{prev}"query{qn}":"{q}",""".format(prev = json_query,
                                                           qn = qnum,
                                                           q = query
                                                           )
        qnum += 1

    json_query = json_query[:-1] + "}"
    return json_query



fql_multi_query = compose_multiquery([
                    fql_friends_on_newsfeed,  # first we get the friends
                    fql_from_list_of_friends.format("SELECT actor_id from #query1"),  # then we query on that list
                    ])

fql_multi_query_fbexample = """{"query1":"SELECT uid2 FROM friend WHERE uid1=me()","query2":"SELECT name FROM user WHERE uid=me()"}""" 
qm1 = "SELECT uid2 FROM friend WHERE uid1=me()"
qm2 = "SELECT  name FROM user WHERE uid=me()"
fql_multi_query_composed = compose_multiquery([qm1,qm2])

f_on_nf = "SELECT actor_id FROM stream WHERE filter_key in ( Select filter_key from stream_filter where uid = me() AND type in ('newsfeed')) AND strpos(attachment.href, \"youtu\") >= 0 LIMIT 10000 "



# this based2 works
f_based2 = """SELECT message, actor_id, created_time FROM stream WHERE source_id in (SELECT uid2 FROM friend WHERE uid1 == me()) LIMIT 10000"""
# this based is not working, complains about {
f_based = """SELECT message, actor_id, created_time, attachment.href, attachment.name, attachment.description, attachment.media.src FROM stream WHERE source_id in (SELECT uid2 FROM friend WHERE uid1 == me()) and strpos(attachment.href, "youtu") >= 0 LIMIT 10000"""

# trying to do a normal query with multi query instead of nested
fql_multi_query2 = compose_multiquery([
                    qm2, # example of another query
                    f_based2 # it works
])
