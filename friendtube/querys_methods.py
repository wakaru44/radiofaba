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



