#!/usr/bin/env python
################################################################################
#    List of queryes for easy retrieval
################################################################################

################################################################################
#   Get friends querys
################################################################################
fql_friends = """
            SELECT uid2
                FROM friend
                WHERE uid1 == me()
"""

# Get the friends that also use the app, and its pictures
graph_friends = "me/friends?fields=name,id,picture"

# Get the list of friends (not only the ones that use the app)
graph_friends_nonapp = "me/taggable_friends"

# get the pic of a friend. REQUIRES a parameter
graph_pic = "{facebookId}/picture?type=square"

################################################################################
#   Get videos querys
################################################################################
# old query to get the results of your. better results with the 1.0 api. almost
# nothing with 2.0 api.
friends_based = """
        SELECT
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


# This query seems to retrieve a lot of duplicates
# And doesn't seem to get more results than the plain nf
filters_based01 = """ 
SELECT 
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

# This one gets the newsfeed only from fql.
filters_newsfeed = """
SELECT 
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
and strpos(attachment.href,"youtu") >= 0
LIMIT 10000
"""

# This one gets the videos of the user
fql_ownvideos = """
SELECT 
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
fql_ownvideos_rest = """
SELECT 
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
