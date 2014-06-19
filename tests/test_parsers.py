from nose.tools import assert_raises,eq_,raises,assert_true,ok_,nottest
from mock import Mock, MagicMock, patch

import friendtube.parsers as pr

## class test_get_embed_youtube():
##     def test_nothing_raises_exception(self):
##         assert_raises(AssertionError,pr.get_embed_youtube)
## 
##     def test_emptystr_raises_exception(self):
##         assert_raises(AssertionError,pr.get_embed_youtube,"")
## 
##     def test_mixed_link(self):
##         tst="https://www.youtube.com/watch?v=18NmQEA5lzo&feature=youtu.be"
##         exp="http://www.youtube.com/embed/18NmQEA5lzo?enablejsapi=1&wmode=opaque"
##         res = pr.get_embed_youtube(tst)
##         eq_(res, exp)
## 
##     @raises(NotImplementedError)
##     def test_malformed_link(self):
##         pr.get_embed_youtube("youtu.be/caca?bar")
## 
##     def test_normal_link(self):
##         exp = 'http://www.youtube.com/embed/Xatb2rh3EBw?enablejsapi=1&wmode=opaque'
##         tst = 'https://www.youtube.com/watch?v=Xatb2rh3EBw'
##         res = pr.get_embed_youtube(tst)
##         eq_(res, exp)
## 
##     def test_dirty_link(self):
##         exp = 'http://www.youtube.com/embed/dBwMQAaLUoY?enablejsapi=1&wmode=opaque'
##         tst = 'http://www.youtube.com/watch?v=dBwMQAaLUoY&feature=player_embedded'
##         res = pr.get_embed_youtube(tst)
##         eq_(res, exp)
## 
##     def test_short_unsafe_link(self):
##         exp = 'http://www.youtube.com/embed/_gWc17vhSAE?enablejsapi=1&wmode=opaque'
##         tst = 'http://youtu.be/_gWc17vhSAE'
##         res = pr.get_embed_youtube(tst)
##         eq_(res, exp)
## 
##     def test_short_safe_link(self):
##         exp = 'http://www.youtube.com/embed/_gWc17vhSAE?enablejsapi=1&wmode=opaque'
##         tst = 'https://youtu.be/_gWc17vhSAE'
##         res = pr.get_embed_youtube(tst)
##         eq_(res, exp)
## 
##     def test_attribution_unsafe_link(self):
##         exp = 'http://www.youtube.com/embed/rSxIk9Qzmmw?enablejsapi=1&wmode=opaque'
##         tst = 'http://www.youtube.com/attribution_link?a=gvouc-iy_pw&u=%2Fwatch%3Fv%3DrSxIk9Qzmmw%26feature%3Dshare'
##         res = pr.get_embed_youtube(tst)
##         eq_(res, exp)
## 
##     @raises(NotImplementedError)
##     def test_attribution_another_link(self):
##         exp = 'http://www.youtube.com/embed/?enablejsapi=1&wmode=opaque'
##         tst = 'http://www.youtube.com/attribution_link?a=xQgZSJGi75Q&u=%2Fplaylist%3Flist%3DPLF72C3E0A45E3093C'
##         res = pr.get_embed_youtube(tst)
##         eq_(res, exp)
## 
##     def test_attribution_safe_link(self):
##         exp = 'http://www.youtube.com/embed/rSxIk9Qzmmw?enablejsapi=1&wmode=opaque'
##         tst = 'https://www.youtube.com/attribution_link?a=gvouc-iy_pw&u=%2Fwatch%3Fv%3DrSxIk9Qzmmw%26feature%3Dshare'
##         res = pr.get_embed_youtube(tst)
##         eq_(res, exp)
## 
##     def test_ampersand_link(self):
##         exp = 'http://www.youtube.com/embed/Zf-YtUuYCDE?enablejsapi=1&wmode=opaque'
##         tst = 'https://www.youtube.com/watch?v=Zf-YtUuYCDE#t=289'
##         res = pr.get_embed_youtube(tst)
##         eq_(res, exp)
## 
##     def test_featured_youtube_short(self):
##         exp = 'http://www.youtube.com/embed/WtnD8VNEk6c?enablejsapi=1&wmode=opaque'
##         tst = 'http://www.youtube.com/watch?v=WtnD8VNEk6c&feature=youtu.be'
##         res = pr.get_embed_youtube(tst)
##         eq_(res, exp)
## 
##     def test_reversed_order_featured(self):
##         exp = 'http://www.youtube.com/embed/xTiF7Hk8NAU?enablejsapi=1&wmode=opaque'
##         tst = 'https://www.youtube.com/watch?feature=player_embedded&v=xTiF7Hk8NAU'
##         res = pr.get_embed_youtube(tst)
##         eq_(res, exp)



class test_get_embed_generic():
## Instead of raising, now we just return None in case of empty
##    def test_nothing_raises_exception(self):
##        assert_raises(AssertionError,pr.get_embed)
##
##    def test_emptystr_raises_exception(self):
##        assert_raises(AssertionError,pr.get_embed,"")

    def test_nothing_returns_nothing(self):
        """returns None when we give None"""
        eq_(pr.get_embed(None), None)

    def test_empty_string_returns_none(self):
        """returns None when we give empty string"""
        eq_(pr.get_embed(""), None)

    @raises(NotImplementedError)
    def test_provider_NI(self):
        pr.get_embed("http://vimeo.com/caca?bar")

    def test_normal_link(self):
        exp = 'http://www.youtube.com/embed/Xatb2rh3EBw?enablejsapi=1&wmode=opaque'
        tst = 'https://www.youtube.com/watch?v=Xatb2rh3EBw'
        res = pr.get_embed(tst)
        eq_(res, exp)


# Disabled. Im not sure this is really relevant test.
#    def test_embebed_link(self):
#        tst = 'http://www.youtube.com/embed/P_qPBiBIjP4?enablejsapi=1&wmode=opaque'
#        res = pr.get_embed_youtube(tst)
#        eq_(res, tst)




class test_parse_fb_result_listing():
    def test_normal_attachment(self):
        data = { "data":[{u'created_time': 1400579416, u'message': u'Independientemente de si estamos de acuerdo con la cultura arabe o no... \xa1Que preciosos cantos devocionales tienen! \n', u'actor_id': u'642011599209080', u'attachment': {u'media': [{u'src': u'https://fbexternal-a.akamaihd.net/safe_image.php?d=AQAIeVp8w3tE46_Y&w=130&h=130&url=http%3A%2F%2Fi1.ytimg.com%2Fvi%2FWaomfpL7gIU%2Fhqdefault.jpg'}], u'href': u'https://www.youtube.com/watch?v=WaomfpL7gIU&index=4&list=LL-P6qSxOejC1KtbnEQuNtuA', u'name': u'From Srat Al-Kahf by Abo Bakr Shatri', u'description': u'From Srat Al-Kahf by Abo Bakr Shatri'}}
]}
        result = pr.parse_fb_result_listing(data)
        eq_(result[0]["preview"] , data["data"][0]["attachment"]["media"][0]["src"])

    def test_empty_src_media(self):
        data = { "data":[{u'created_time': 1400532456, u'message': u'https://www.youtube.com/watch?v=MkYyG1GOETc', u'actor_id': u'10152038751900976', u'attachment': {u'media': [{u'src': u''}], u'href': u'https://www.youtube.com/watch?v=MkYyG1GOETc', u'name': u'The Riptides - 77 Sunset Strip (1979)', u'description': u"Music from Australia and New Zealand in the year 1979: The Riptides' promo-video for the single 'Sunset Strip' (July, 1979). Band Location: Brisbane, QLD, Au..."}}]}
        result = pr.parse_fb_result_listing(data)
        eq_("" , data["data"][0]["attachment"]["media"][0]["src"])
        eq_(result[0]["preview"] , "/style/preview_default.png")

    def test_empty_at_all_media(self):
        data = { "data":[{u'created_time': 1400500953, u'message': u'Ha sido una mala semana, con muchas cosas encima, y hoy no he empezado bien el d\xeda, pero me da igual francamente...  https://www.youtube.com/watch?v=y6Sxv-sUYtM :) ',
                          u'actor_id': u'10203087889496668', u'attachment':
                          {u'media': [], u'href':
                           u'https://www.youtube.com/watch?v=y6Sxv-sUYtM',
                           u'name': u'www.youtube.com', u'description': u''}}]}
        result = pr.parse_fb_result_listing(data)
        eq_(result[0]["preview"] , u'/style/preview_default.png') #default picture


class BaseTestCase_ParsingElements():
    def setUp(self):
        self.normal_elem =  {u'created_time': 1400500953,
                u'message': u'Ha sido una mala semana, con muchas cosas encima, y hoy no he empezado bien el d\xeda, pero me da igual francamente...  https://www.youtube.com/watch?v=y6Sxv-sUYtM :) ',
                u'actor_id': u'10203087889496668',
                u'attachment': {u'media': [],
                                u'href': u'https://www.youtube.com/watch?v=y6Sxv-sUYtM',
                                u'name': u'www.youtube.com',
                                u'description': u''}}
        self.missing_created =  { u'message': u'Ha sido una mala semana, con muchas cosas encima, y hoy no he empezado bien el d\xeda, pero me da igual francamente...  https://www.youtube.com/watch?v=y6Sxv-sUYtM :) ',
                u'actor_id': u'10203087889496668',
                u'attachment': {u'media': [],
                                u'href': u'https://www.youtube.com/watch?v=y6Sxv-sUYtM',
                                u'name': u'www.youtube.com',
                                u'description': u''}}

        self.missing_actor = {u'created_time': 1400500953,
                u'message': u'Ha sido una mala semana, con muchas cosas encima, y hoy no he empezado bien el d\xeda, pero me da igual francamente...  https://www.youtube.com/watch?v=y6Sxv-sUYtM :) ',
                u'attachment': {u'media': [],
                                u'href': u'https://www.youtube.com/watch?v=y6Sxv-sUYtM',
                                u'name': u'www.youtube.com',
                                u'description': u''}}


class test_parse_created(BaseTestCase_ParsingElements):
    def test_normal_element(self):
        elem = self.normal_elem
        result = pr.parse_created(elem)
        #eq_(result, "2014-05-19 14:02")  # this is not timezone sensible. GMT + 2
        eq_(result, "2014-05-19 12:02")  # this is not timezone sensible. GMT + 2

    def test_nonexistant_element(self):
        elem = self.missing_created
        result = pr.parse_created(elem)
        eq_(result, "Disabled")



class test_parse_actor(BaseTestCase_ParsingElements):
    def test_normal_element(self):
         elem = self.normal_elem
         result = pr.parse_actor(elem)
         eq_(result, [u'10203087889496668'])

    def test_nonexistant_element(self):
        elem = self.missing_actor
        result = pr.parse_actor(elem)
        eq_(result, [u'Disabled'])



class test_parse_preview(BaseTestCase_ParsingElements):
    def test_returns_default_on_none(self):
        eq_(pr.parse_preview(None), u'/style/preview_default.png')

    def test_gets_the_preview_picture(self):
        elem = {u'created_time': 1400579416, u'message': u'Independientemente de si estamos de acuerdo con la cultura arabe o no... \xa1Que preciosos cantos devocionales tienen! \n', u'actor_id': u'642011599209080', u'attachment': {u'media': [{u'src': u'existant_preview.jpg'}], u'href': u'https://www.youtube.com/watch?v=WaomfpL7gIU&index=4&list=LL-P6qSxOejC1KtbnEQuNtuA', u'name': u'From Srat Al-Kahf by Abo Bakr Shatri', u'description': u'From Srat Al-Kahf by Abo Bakr Shatri'}}
        result = pr.parse_preview(elem)
        eq_(result, u'existant_preview.jpg')

    def test_if_no_preview_use_default_picture(self):
        elem = self.missing_actor
        result = pr.parse_preview(elem)
        eq_(result, u'/style/preview_default.png')


class test_parse_description():
    def setUp(self):
        self.normal_elem = {u'created_time': 1400579416, u'message': u'the message', u'actor_id': u'642011599209080', u'attachment': {u'media': [{u'src': u'https://fbexternal-a.akamaihd.net/safe_image.php?d=AQAIeVp8w3tE46_Y&w=130&h=130&url=http%3A%2F%2Fi1.ytimg.com%2Fvi%2FWaomfpL7gIU%2Fhqdefault.jpg'}], u'href': u'https://www.youtube.com/watch?v=WaomfpL7gIU&index=4&list=LL-P6qSxOejC1KtbnEQuNtuA', u'name': u'From Srat Al-Kahf by Abo Bakr Shatri', u'description': u'the description'}}
        self.long_message_elem = {u'created_time': 1400579416, u'message': u'very very very very very very very very very very very very very very very very very very very long message, more than 100 chars long', u'actor_id': u'642011599209080', u'attachment': {u'media': [{u'src': u'https://fbexternal-a.akamaihd.net/safe_image.php?d=AQAIeVp8w3tE46_Y&w=130&h=130&url=http%3A%2F%2Fi1.ytimg.com%2Fvi%2FWaomfpL7gIU%2Fhqdefault.jpg'}], u'href': u'https://www.youtube.com/watch?v=WaomfpL7gIU&index=4&list=LL-P6qSxOejC1KtbnEQuNtuA', u'name': u'From Srat Al-Kahf by Abo Bakr Shatri', u'description': u'the description'}}
        self.long_desc_elem = {u'created_time': 1400579416, u'message': u'the message', u'actor_id': u'642011599209080', u'attachment': {u'media': [{u'src': u'preview_picture.jpg'}], u'href': u'http://youtube/link', u'name': u'lorem ipsum', u'description': u'the description'}}
        self.missing_desc_and_message = {u'created_time': 1400579416, u'actor_id': u'642011599209080', u'attachment': {u'media': [{u'src': u'https://fbexternal-a.akamaihd.net/safe_image.php?d=AQAIeVp8w3tE46_Y&w=130&h=130&url=http%3A%2F%2Fi1.ytimg.com%2Fvi%2FWaomfpL7gIU%2Fhqdefault.jpg'}], u'href': u'https://www.youtube.com/watch?v=WaomfpL7gIU&index=4&list=LL-P6qSxOejC1KtbnEQuNtuA', u'name': u'From Srat Al-Kahf by Abo Bakr Shatri'}}

    def test_it_get_the_description_from_message_and_description(self):
        elem = self.normal_elem
        result = pr.parse_description(elem)
        eq_(result, u'the description\n<br />\n ---------------------<br /> the message')

    def test_long_messages_must_be_trimmed(self):
        """trim the fb message if it is too long"""
        elem = self.long_message_elem
        result = pr.parse_description(elem)
        eq_(result, u'the description\n<br />\n ---------------------<br /> very very very very very very very very very very very very very very very very very very very long <span class=\"greyed\">... For more check your timeline</span>')

    def test_long_descriptions_must_be_trimmed(self):
        """trim the youtube description if it is too long"""
        elem = self.long_desc_elem
        result = pr.parse_description(elem)
        eq_(result, u'the description\n<br />\n ---------------------<br /> the message')

    def test_return_none_on_none(self):
        eq_(pr.parse_description(None),None)

    def test_return_none_on_missing_elements(self):
        elem = self.missing_desc_and_message
        result = pr.parse_description(elem)
        eq_(result, None)


class test_clean_list_removes_duplicates():
    def setUp(self):
        self.data = [{'actor': [u'786664311344363'],
                   'created': '2014-05-20 15:59',
                   'desc': u'\n<br />\n ---------------------<br /> ',
                   'link': 'http://www.youtube.com/embed/gSCj6vlei8Y?enablejsapi=1&wmode=opaque',
                   'preview': u'httph=130&url=http%3A%2F%2Fi1.ytimg.com%2Fvi%2FgSCj6vlei8Y%2Fmaxresdefault.jpg',
                   'title': u'Concuso de Cosplay Expomanga Madrid 2014.  Actuaci\xf3n 25 -- Saint Seya'},
                {'actor': [u'277680312412688'],
                   'created': '2014-05-20 12:58',
                   'desc': u'\n<br />\n ---------------------<br gSCj6vlei8Y',
                   'link': 'http://www.youtube.com/embed/gSCj6vlei8Y?enablejsapi=1&wmode=opaque',
                   'preview': u'ht=130&h=130&url=http%3A%2F%2Fi1.ytimg.com%2Fvi%2FgSCj6vlei8Y%2Fmaxresdefault.jpg',
                   'title': u'Concuso de Cosplay Expomanga Madrid 2014.  Actuaci\xf3n 25 -- Saint Seya'},
                {'actor': [u'10203220863658071'],
                   'created': '2014-05-20 14:52',
                   'desc': u': A los 15 a\xf1os Adele (Ad\xe8le Exarchopoulos) Martes de cine, a las 21:00h.',
                   'link': 'http://www.youtube.com/embed/XBzEMlRV5WI?enablejsapi=1&wmode=opaque',
                   'preview': u'https%2F%2Fi1.ytimg.com%2Fvi%2FXBzEMlRV5WI%2Fmaxresdefault.jpg',
                   'title': u'La vida de Adele - Trailer en espan\u0303ol (HD)'}] 


    @nottest
    def test_long_list(self):
        #TODO: try to replicate an index out of range when we delete more than
        # not the last element but one in the middle
        assert("this" == "valid")



    def test_clean_list_reduces_a_list_with_duplicates(self):
        things = self.data
        clean = pr.clean_list(things)
        eq_(len(clean), 2)

    @nottest
    def test_add_actors(self):
        #TODO: write this test
        things = self.data
        clean = pr.clean_list(things)
        print len(clean)
        assert("this" == "valid")

