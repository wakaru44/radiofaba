#!/usr/bin/env python

# List of queryes for easy retrieval

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
