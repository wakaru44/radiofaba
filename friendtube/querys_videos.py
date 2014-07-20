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


#Experimental. take videos from vimeo. 
fql_vimeo_videos_from_nf = """SELECT 
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
and strpos(attachment.href,"vimeo") >= 0
LIMIT 5000
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

#EXperimental. 
# retrieves the facebook videos (not youtube) and the attributes.
fql_fbvideos_from_newsfeed="""SELECT
            message,
            actor_id,
            created_time, 
            attachment.href,
            attachment.name,
            attachment.fb_object_type,
            attachment.description,
            attachment.media.src
        FROM stream
        WHERE filter_key in 
            ( 
                    Select filter_key
                        from stream_filter
                        where uid = me() 
                        AND type in ('newsfeed')
            ) 
and 
            attachment.fb_object_type = "video"
        LIMIT 100000
"""


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


# get users own videos.
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


