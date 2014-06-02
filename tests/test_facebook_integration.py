#!/usr/bin/env python

import sys
print sys.path
sys.path.append("./lib")

import unittest
import mock

from nose.tools import assert_raises,eq_,raises,assert_true,ok_, nottest

import facebook

class BaseTest(unittest.TestCase):
    pass

def call_to(thing):
    print "calling smthng"
    return thing()

class test_passmock(BaseTest):
    def test_call_mock(self):
        myMock = mock.Mock()
        print myMock
        myMock("fooo")
        assert(myMock.called== True)

    def test_inject_simple_mock(self):
        myMock=mock.MagicMock()
        print myMock
        myMock.myMethod = mock.Mock(return_value= "im back")
        eq_(call_to(myMock.myMethod),"im back")

    def test_calling_module_methods(self):
        result = facebook.auth_url(
            app_id="foo", 
            canvas_url = "http://apps.facebook.com/friend-tube",
            perms=None,
            version="v2.0"
            )
        eq_(result,
            "https://www.facebook.com/v2.0/dialog/oauth?redirect_uri=http%3A%2F%2Fapps.facebook.com%2Ffriend-tube&client_id=foo")

    @mock.patch('facebook.requests')
    def test_mocking_call_to_request(self, mock):
        """Try to mock the requests module"""
        # requests = mock.MagicMock()
        # requests.request(return_value = "Success")
        # requests.GraphAPI(return_value = "Success")
        # #print "original: " + repr(dir(facebook.requests))
        # facebook.requests = requests
        # #requests = requests
        # #print "mocked: " + repr(dir(facebook.requests))
        # #fb = facebook.GraphAPI()
        # facebook.GraphAPI = requests
        fb = facebook.GraphAPI("whatever")
        call = fb.get_app_access_token("app_id","app_secret")
        
        print "fb" + repr(fb)
        print "called rq: " + repr(facebook.requests.called)
        print "called mk: " + repr(mock.called)
        print "args: " + repr(facebook.requests.call_args)
        print "args: " + repr(mock.call_args)
        eq_(facebook.requests, # TODO: useless test
            "https://www.facebook.com/v2.0/dialog/oauth?redirect_uri=http%3A%2F%2Fapps.facebook.com%2Ffriend-tube&client_id=foo")

