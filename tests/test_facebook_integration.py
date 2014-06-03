#!/usr/bin/env python

import sys
print sys.path
sys.path.append("./lib")
sys.path.append("../../google_appengine")

import unittest
import mock

from nose.tools import assert_raises,eq_,raises,assert_true,ok_, nottest

import facebook
import friendtube
from friendtube.BaseHandler import BaseHandler as BH

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

    @mock.patch('facebook.GraphAPI')
    def test_mocking_call_to_graphapi(self, mock = None):
        """Try to mock the GraphAPI  module"""
        mock.return_value("""Response from facebook""")
        fb = facebook.GraphAPI()
        call = fb.get_app_access_token("app_id","app_secret")

        eq_(fb.called,True)
        #assert(fb.assert_any_call("get_app_access_token") == True)
        #eq_(fb.call_args , "xxx")
        #eq_(fb.assert_any_call('Response from facebook', True))
        #eq_(fb.assert_any_call('Response from facebook'), True)


    @mock.patch('facebook.GraphAPI.get_access_token_from_code')
    def test_mocking_call_to_submodule_graphapi(self, mock = None):
        """Try to mock a submodule"""
        #mock.get_app_access_token = mock.MagicMock(return_value = "mocked token")
        mock.return_value = "fake Token"
        fb = facebook.GraphAPI()
        result = fb.get_access_token_from_code("app_id","app_secret")

        eq_(fb.get_access_token_from_code.called,True)
        eq_(result , "fake Token") #- we are trying to return something expected
                                     #- mocking inside facebook.GraphAPI


    @nottest
    @mock.patch('facebook.GraphAPI.get_access_token_from_code')
    def test_mocking_submodule_and_calling_other(self, mock = None):
        """Testing the effect of mocking submodule and here call another"""
        mock.return_value = "fake Token"
        fb = facebook.GraphAPI()
        result = facebook.get_user_from_cookie({"cookies":"nothing"},"app_id","app_secret" )

        eq_(fb.get_access_token_from_code.called,True)
        eq_(result , "fake Token") #- we are trying to return something expected
                                     #- mocking inside facebook.GraphAPI


    @nottest
    @mock.patch('facebook.GraphAPI.request')
    def test_mocking_call_to_request(self, mock):
        """Try to mock an inner module"""
        # requests = mock.MagicMock()
        # requests.request(return_value = "Success")
        # requests.GraphAPI(return_value = "Success")
        # #print "original: " + repr(dir(facebook.requests))
        # facebook.requests = requests
        # #requests = requests
        # #print "mocked: " + repr(dir(facebook.requests))
        # #fb = facebook.GraphAPI()
        # facebook.GraphAPI = requests
        from requests.structures import CaseInsensitiveDict
        fake_headers = CaseInsensitiveDict({'content-type': 'application/json; charset=UTF-8', 'x-fb-rev': '1272240', 'date': 'Mon, 02 Jun 2014 17:08:54 GMT', 'expires': 'Sat, 01 Jan 2000 00:00:00 GMT', 'etag': '"84c04345f74471f3b7e5f9f721ac765c01481f34"', 'cache-control': 'private, no-cache, no-store, must-revalidate', 'content-length': '2735', 'pragma': 'no-cache', 'access-control-allow-origin': '*', 'connection': 'keep-alive', 'content-encoding': 'gzip', 'x-fb-debug': 'yiplc1Vj8GzQYRzMKG1yCMkouUBL68SbleOG0uTahfA='})
        fake_encoding = "UTF-8"
        fake_text = "lots of text with things like json"
        fake_status_code = "200L" #float?
        fake_url = "url of the query done to facebook"

        #foo =  {u'data': [{u'name': u'Dorota Z Ziemi', u'picture': {u'data': {u'url': u'https://scontent-a.xx.fbcdn.net/hprofile-xpf1/l/t1.0-1/c0.0.50.50/p50x50/984046_754398587913703_6886081788577219115_n.jpg', u'is_silhouette': False}}, u'id': u'100000307053246'}], u'paging': {u'next': u'https://graph.facebook.com/v2.0/739393348/friends?fields=name,id,picture&access_token=CAAHbF03ounQBALi93FVt8Vlfquiv2AZCr2VdBHwUWubgryYEc2QddsA0dXG574seZCucRMIOMtIBG6my0ZBrRYLJSxmZBTdA8E4n9Lhc37IqYQ3GloqGsSCnZBRP3BxFenodX0Q6PHKsjJEhGk7yjAmzYgJfzfbOhItWbksEOcHWJAWIkEsGqExgbJlBbusMZD&limit=5000&offset=5000&__after_id=enc_AewwxFTtDL5rKVMDXWeqH0SQd3p3kXS2Py0vIS7kocl-hSTKScKUNYZsn818LDIHu2wiUWw6y1DzIeshOwEf_Puk'}}
        mock.headers = "faaaakeeee"
        mock.encoding = fake_encoding
        mock.text = fake_text
        mock.status_code = fake_status_code
        mock.url(return_value = fake_url)
        fb = facebook.GraphAPI()
        call = fb.get_app_access_token("app_id","app_secret")
        
        print "fb" + repr(fb)
        print "called rq: " + repr(facebook.requests.called)
        print "called mk: " + repr(mock.called)
        print "args: " + repr(facebook.requests.call_args)
        print "args: " + repr(mock.call_args)
        eq_(facebook.requests, # TODO: useless test
            "https://www.facebook.com/v2.0/dialog/oauth?redirect_uri=http%3A%2F%2Fapps.facebook.com%2Ffriend-tube&client_id=foo")


    #@mock.patch('friendtube.BaseHandler.facebook.get_user_from_cookie')
    @mock.patch('friendtube.BaseHandler.BaseHandler.do_query')
    def test_mocking_lib_in_our_code(self, mock = None):
        """Try to mock the facebook library"""
        #mock.get_app_access_token = mock.MagicMock(return_value = "mocked token")
        exp_res = {"name":"fake name", "uid":"70000007"}
        mock.return_value = exp_res
        app = BH()
        result = app.do_query("/me")

        eq_(result , exp_res) #- we are trying to return something expected
                                     #- mocking inside facebook.GraphAPI
        eq_(mock.called, True)

    @mock.patch('friendtube.BaseHandler.BaseHandler.current_user')
    def test_all_patches_necesary(self,mock = None):
        """Try to get all call to facebook mocked module"""
        app = BH()
        print dir(app)
        #app.app.active_instance.request.application_url = mock.MagikMock()
        fake_user = {"key_name":"",
                     "id":"",
                     "name":"",
                     "profile_url":"",
                     "access_token":""}
        mock.return_value = fake_user
        #mock.patch("friendtube.BaseHandler.facebook.GraphAPI.fql", return_value = "fakereturn")
        fake_content = {u'data':
                            [{u'actor_id': u'739393348',
                              u'created_time': 1401493234,
                              u'message': u'',
                              u'attachment':
                                  {u'name': u'Fanfarria Taquikardia',
                                   u'media': [{u'src': u'https://fbexternal-2Fmaxresdefault.jpg'}],
                                   u'description': u'Galiza, Outono se ...',
                                   u'href': u'http://www.youtube.com/watch?v=Hm8PkBHkUVE&feature=youtu.be'}
                             }]
                       }
        fake_result = {}
        friendtube.BaseHandler.facebook.GraphAPI.fql = mock.MagicMock( return_value = fake_content)
        friendtube.BaseHandler.rparse = mock.MagicMock( return_value = fake_content)
        friendtube.BaseHandler.current_user = mock.MagicMock( return_value = fake_user )
        friendtube.BaseHandler.rparse.clean_list = mock.MagicMock( return_value = fake_result)

        result = app.get_video_listing()
        eq_(friendtube.BaseHandler.rparse.called, True)
        # friendtube.BaseHandler.rparse.reset_mock() # If i reset one of the
        # mocks, both are reset
        eq_(friendtube.BaseHandler.facebook.GraphAPI.fql.called, True)
        #eq_(friendtube.BaseHandler.facebook.GraphAPI.fql.call_args, True)
        eq_(result, "fake_result") 
        ## AssertionError: <MagicMock name='current_user.MagicMock()()' id='139788364583376'> != 'fake_result'
        #TODO: write something that works...
