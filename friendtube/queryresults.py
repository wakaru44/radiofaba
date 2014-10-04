friends_on_nf = { "data": [
              { "actor_id": "520468721409943" }, 
              { "actor_id": "342714211268" }, 
              { "actor_id": "838894906138604" }, 
              { "actor_id": "12500217831" }, 
              { "actor_id": "10203656285228486" }, 
              { "actor_id": "788799174464444" }, 
              { "actor_id": "10203181079664632" }, 
              { "actor_id": "10204094479910261" }, 
              { "actor_id": "10203087889496668" }
            ] }

fql result: {u'data': [
    {u'name': u'query1',
     u'fql_result_set': [{u'name': u'Wakaru Himura'}]},
    {u'name': u'query2',
     u'fql_result_set': [{u'uid2': u'100000307053246'}]}
]}

==========================================================================

doing Query: '{"query1":"SELECT  name FROM user WHERE uid=me()","query2":"\n      
  SELECT\n            message,\n            actor_id,\n            created_time,\n            attachment.href,\n            attachment.
name,\n            attachment.description,\n            attachment.media.src\n        FROM stream\n        WHERE source_id in\n        
    (SELECT uid2\n                FROM friend\n                WHERE uid1 == me()\n            ) \n            and\n            strpos(
attachment.href, "youtu") >= 0\n        LIMIT 10000\n        "}'
DEBUG    2014-06-19 05:13:05,677 __init__.py:263] the fql is a string

{"query1":"SELECT  name FROM user WHERE uid=me()","query2":"SELECT message, actor_id, created_time, attachment.href, attachment.
name, attachment.description, attachment.media.src FROM stream WHERE source_id in (SELECT uid2 FROM friend WHERE uid1 == me() )             and strpos(
attachment.href, "youtu") >= 0 LIMIT 10000       "}

--------------------------------------


doing Query: '{"query1":"SELECT  name FROM user WHERE uid=me()","query2":"SELECT u
id2 FROM friend WHERE uid1=me()"}'
DEBUG    2014-06-19 05:14:50,393 __init__.py:263] the fql is a string

{"query1":"SELECT uid2 FROM friend WHERE uid1=me()","query2":"SELECT name FROM user WHERE uid=me()"}



======================================================

%7B%22query1%22%3A%22SELECT++name+FROM+user+WHERE+uid%3Dme%28%
29%22%2C%22query2%22%3A%22SELECT+message%2C+actor_id%2C+created_time%2C+attachment.href%2C+attachment.name%2C+attachment.description%2C
+attachment.media.src+FROM+stream+WHERE+source_id+in+%28SELECT+uid2+FROM+friend+WHERE+uid1+%3D%3D+me%28%29%29+and+strpos%28attachment.h
ref%2C+%22youtu%22%29+%3E%3D+0+LIMIT+10000%22%7D


---------------------------------------

GET /v2.0/fql?access_token=CAAHbF03ounQBABVo5qKy3ZCoQXlGqGYFGnMGZAKczCYFge9pNS
IcLzZAaqUwputDgcCK4QHdRJoKlHOtquZCgkueiSYZClDdOTjjEqzFD6KcJcxbLnbXnMRV1GklusMiTQHCa1yZB4lsgCth7aeauPDpyVKA6uHqbbiCwOP0ezaSoE1MgfbfjcADI
gZAPHu7RwZD&q=%7B%22query1%22%3A%22SELECT++name+FROM+user+WHERE+uid%3Dme%28%29%22%2C%22query2%22%3A%22SELECT+uid2+FROM+friend+WHERE+uid
1%3Dme%28%29%22%7D HTTP/1.1" 200 None


======================================================





{"query1":"SELECT  name FROM user WHERE uid=me()","query2":"SELECT message, actor_id, created_time, attachment.href, attachment.name, attachment.description, attachment.media.src FROM stream WHERE source_id in (SELECT uid2 FROM friend WHERE uid1 == me()) and strpos(attachment.href, "youtu") >= 0 LIMIT 10000"}


# simplificando
SELECT message, actor_id, created_time FROM stream WHERE source_id in (SELECT uid2 FROM friend WHERE uid1 == me()) LIMIT 10

{"query1":"SELECT  name FROM user WHERE uid=me()","query2":"SELECT message, actor_id, created_time FROM stream WHERE source_id in (SELECT uid2 FROM friend WHERE uid1 == me()) LIMIT 10"}







# friends in nf
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











