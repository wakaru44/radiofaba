from nose.tools import assert_raises,eq_,raises,assert_true,ok_, nottest

import sys
print sys.path
sys.path.append("./lib")
sys.path.append("/home/wakaru/workspace/google_appengine")

from os import listdir
from os.path import isfile,join

import friendtube.HomeHandlers as HH

class test_HomeHandler_AddOns():
    @nottest
    def test_environment(self):
        print "sys.path"
        print sys.path
        folder = "/home/wakaru/workspace/google_appengine"
        print "listing files only" + folder
        files_only = [ f for f in listdir(folder) if isfile(join(folder,f)) ]
        print files_only
        print "\nlisting" + folder
        dir_content = [ f for f in listdir(folder) if not isfile(join(folder,f)) ]
        print dir_content
        

        assert("show" == True)

    def test_list2html_returns_empty_list(self):
        th = HH.TestHandler()
        result = th.list2html()
        eq_(result, "")

    def test_list2html_returns_1_element(self):
        th = HH.TestHandler()
        result = th.list2html(["1"])
        eq_(result, "<ul>\n<li>1</li>\n</ul>\n")

    def test_list2html_returns_3_elements(self):
        th = HH.TestHandler()
        result = th.list2html(["1","2","3"])
        eq_(result, "<ul>\n<li>1</li>\n<li>2</li>\n<li>3</li>\n</ul>\n")

    def test_list2html_prints_id(self):
        th = HH.TestHandler()
        result = th.list2html(["1"], htmlid = "identifier")
        eq_(result, "<ul id=\"identifier\" >\n<li>1</li>\n</ul>\n")

    def test_list2html_dont_print_id_or_class(self):
        th = HH.TestHandler()
        result = th.list2html(["1"])
        eq_(result, "<ul>\n<li>1</li>\n</ul>\n")

    def test_list2html_prints_class(self):
        th = HH.TestHandler()
        result = th.list2html(["1"], htmlclass = "classic")
        eq_(result, "<ul class=\"classic\" >\n<li>1</li>\n</ul>\n")

