#!/usr/bin/env python
################################################################################
#    List of queryes for easy retrieval
################################################################################

from querys_friends import *
from querys_videos import *
from querys_archive import *
from querys_methods import *


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

########################################
#   Multi Querys
########################################

fql_multi_query = compose_multiquery([
                    fql_friends_on_newsfeed,  # first we get the friends
                    fql_from_list_of_friends.format("SELECT actor_id from #query1"),  # then we query on that list
                    ])


# trying to do a normal query with multi query instead of nested
fql_multi_query2 = compose_multiquery([
                    qm2, # example of another query
                    f_based2 # it works
])


########################################
#   composed querys
########################################

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


