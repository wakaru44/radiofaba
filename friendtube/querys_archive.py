
# this based2 works
f_based2 = """SELECT message, actor_id, created_time FROM stream WHERE source_id in (SELECT uid2 FROM friend WHERE uid1 == me()) LIMIT 10000"""
# this based is not working, complains about {
f_based = """SELECT message, actor_id, created_time, attachment.href, attachment.name, attachment.description, attachment.media.src FROM stream WHERE source_id in (SELECT uid2 FROM friend WHERE uid1 == me()) and strpos(attachment.href, "youtu") >= 0 LIMIT 10000"""



fql_multi_query_fbexample = """{"query1":"SELECT uid2 FROM friend WHERE uid1=me()","query2":"SELECT name FROM user WHERE uid=me()"}""" 
qm1 = "SELECT uid2 FROM friend WHERE uid1=me()"
qm2 = "SELECT  name FROM user WHERE uid=me()"
fql_multi_query_composed = compose_multiquery([qm1,qm2])

f_on_nf = "SELECT actor_id FROM stream WHERE filter_key in ( Select filter_key from stream_filter where uid = me() AND type in ('newsfeed')) AND strpos(attachment.href, \"youtu\") >= 0 LIMIT 10000 "
