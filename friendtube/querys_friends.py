
################################################################################
#   Helper querys (other info from friends)
################################################################################

# get the pic of a friend. REQUIRES a parameter
graph_pic = "{facebookId}/picture?type=square"


fql_friends_profiles = """SELECT
name, id, pic_square
FROM profile
WHERE id in ({0})
"""



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
    strpos(attachment.href, 'youtu') >= 0
LIMIT 10000
"""


################################################################################
################################################################################
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

fql_list_of_good_source_friends_and_others = """SELECT
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
                    )
                AND
                    strpos(attachment.href, 'youtu') >= 0
                LIMIT 10000
            ) 
        AND
            strpos(attachment.href, 'youtu') >= 0
        LIMIT 100000
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
                LIMIT 100000
            ) 
        AND
            strpos(attachment.href, 'youtu') >= 0
        LIMIT 1000000
"""

