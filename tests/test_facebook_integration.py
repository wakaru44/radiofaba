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
from friendtube.ListHandlers import ListHandler as LH
import friendtube.sampleresult as stored_sample

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



################################################################################
#   List Handler tests
################################################################################
class test_List_Handler(BaseTest):
    @mock.patch('friendtube.ListHandlers.ListHandler.do_query')
    def test_mock_do_query(self, mock = None):
        """test pass if we can change do_query method on get list"""
        lh = LH()
        sample = {"data":[{"name":"aname"}]}
        mock.return_value = sample
        result = lh.do_query("/me")
        eq_(result,sample)


class test_List_HandlerMocking(BaseTest):
    def setUp(self):
        """Creating the most used mocks"""
        # sample data
        self.fake_user = {"key_name":"",
                     "id":"",
                     "name":"",
                     "profile_url":"",
                     "access_token":""}
        self.fake_content = {u'data':
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
        self.fake_result = {}

        # mocks
        friendtube.ListHandlers.ListHandler.render = mock.MagicMock()
        friendtube.ListHandlers.rparse = mock.MagicMock( return_value = self.fake_content) # probando mierdas
        friendtube.BaseHandler.BaseHandler.current_user = mock.MagicMock( return_value = self.fake_user ) # the user

    @mock.patch('friendtube.ListHandlers.ListHandler.do_query')
    @raises(AssertionError)  # TODO: find a better way to assert the redirect
    def test_call_to_get_with_relogin_do_query_results_returns_redirect(self, mock = None):
        """Verify that get sends us to the logout page if we are logged out"""
        lh = LH()
        sample = {"data":[{"bar":"foo"}],"error":"Please relogin again"}
        mock.return_value = sample
        result = lh.get()
        eq_(result,sample)

    @mock.patch('friendtube.ListHandlers.ListHandler.do_query')
    def test_call_to_get_with_relogin_do_query_results_returns_redirect2(self, mock = None):
        """Verify that get sends us to the logout page if we are logged out 2"""
        lh = LH()
        sample = {"data":[{"bar":"foo"}],"error":"Please relogin again"}
        mock.return_value = sample
        friendtube.ListHandlers.ListHandler.redirect = mock.MagicMock(return_value = None)
        result = lh.get()
        eq_(friendtube.ListHandlers.ListHandler.redirect.called, True)

    @mock.patch('friendtube.ListHandlers.ListHandler.do_query')
    def test_loads_correctly_with_correct_data(self, local_mock = None):
        """Load correct results when correct data provided"""
        # mock def
        stored_data = stored_sample.result_works
        local_mock.return_value = { "data":stored_data["data"], "error":""}

        # task
        lh = LH()
        lh.get()

        # assertions
        eq_(local_mock.called , True)
        eq_(friendtube.ListHandlers.ListHandler.render.called, True)

################################################################################
#   More facebook and listHandler mocking
################################################################################
class test_facebook_mocking_2(BaseTest):
    def setUp(self):
        self.fake_user = {"key_name":"",
                     "id":"",
                     "name":"",
                     "profile_url":"",
                     "access_token":""}
        self.fake_content = {u'data':
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
        self.fake_result = {}
        self.fake_query_result = {"data":self.fake_content["data"], "error":""}


        #friendtube.ListHandlers.facebook.GraphAPI.fql = mock.MagicMock( return_value = self.fake_content) # probando app fb
        friendtube.ListHandlers.rparse = mock.MagicMock( return_value = self.fake_content) # probando mierdas
        friendtube.ListHandlers.rparse.clean_list = mock.MagicMock( return_value = self.fake_content) # probando mierdas
        #friendtube.ListHandlers.rparse.clean_list = mock.MagicMock( return_value = fake_content) # the content in dict format
        friendtube.BaseHandler.BaseHandler.current_user = mock.MagicMock( return_value = self.fake_user ) # the user
        friendtube.BaseHandler.BaseHandler.do_query = mock.MagicMock( return_value = self.fake_query_result ) # the query result

    def test_all_patches_necesary(self):
        """Try to get all call to facebook mocked module"""

        #- mocks definitions
        #mock.return_value = fake_user
        #mock.return_value = fake_content

        app = LH()
        print dir(app)
        result = app.get_video_listing()
        expected_call = mock.call(
                        {
                            'playlist': mock.MagicMock(name='mock.clean_list()', id='139655266612240'),
                            'error': ''
                        },
                        'player-0.2b.html',
                        user=mock.MagicMock()
                        )

        #- assertions
        eq_(friendtube.ListHandlers.rparse.clean_list.called, True)
        eq_(friendtube.ListHandlers.ListHandler.do_query.called, True)
        eq_(friendtube.ListHandlers.ListHandler.render.called, True)
        #eq_(repr(friendtube.ListHandlers.ListHandler.render.call_args)[5:-1], repr(expected_call))  # imposible to test like this
        # friendtube.BaseHandler.rparse.reset_mock() # If i reset one of the mocks, both are reset



class test_facebook_mocking_example(BaseTest):
    @mock.patch('friendtube.ListHandlers.ListHandler.get')
    def test_mock_example(self, local_mock = None):
        """mocking example"""
        # mock def
        stored_data = "fake value"
        local_mock.return_value = stored_data

        # task
        lh = LH()
        result = lh.get()

        # info
        print local_mock.called
        print local_mock.call_args

        eq_(local_mock.called, True)
        eq_(result, stored_data)

