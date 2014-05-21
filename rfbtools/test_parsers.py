from nose.tools import assert_raises,eq_,raises,assert_true,ok_

import rfbtools.parsers as pr

class test_get_embed_youtube():
    def test_nothing_raises_exception(self):
        assert_raises(AssertionError,pr.get_embed_youtube)

    def test_emptystr_raises_exception(self):
        assert_raises(AssertionError,pr.get_embed_youtube,"")

# Disabled. Im not sure this is really relevant test.
#    def test_embebed_link(self):
#        tst = 'http://www.youtube.com/embed/P_qPBiBIjP4?enablejsapi=1&wmode=opaque'
#        res = pr.get_embed_youtube(tst)
#        eq_(res, tst)

    def test_mixed_link(self):
        tst="https://www.youtube.com/watch?v=18NmQEA5lzo&feature=youtu.be"
        exp="http://www.youtube.com/embed/18NmQEA5lzo?enablejsapi=1&wmode=opaque"
        res = pr.get_embed_youtube(tst)
        eq_(res, exp)

    @raises(NotImplementedError)
    def test_malformed_link(self):
        pr.get_embed_youtube("youtu.be/caca?bar")

    def test_normal_link(self):
        exp = 'http://www.youtube.com/embed/Xatb2rh3EBw?enablejsapi=1&wmode=opaque'
        tst = 'https://www.youtube.com/watch?v=Xatb2rh3EBw'
        res = pr.get_embed_youtube(tst)
        eq_(res, exp)

    def test_dirty_link(self):
        exp = 'http://www.youtube.com/embed/dBwMQAaLUoY?enablejsapi=1&wmode=opaque'
        tst = 'http://www.youtube.com/watch?v=dBwMQAaLUoY&feature=player_embedded'
        res = pr.get_embed_youtube(tst)
        eq_(res, exp)

    def test_short_unsafe_link(self):
        exp = 'http://www.youtube.com/embed/_gWc17vhSAE?enablejsapi=1&wmode=opaque'
        tst = 'http://youtu.be/_gWc17vhSAE'
        res = pr.get_embed_youtube(tst)
        eq_(res, exp)

    def test_short_safe_link(self):
        exp = 'http://www.youtube.com/embed/_gWc17vhSAE?enablejsapi=1&wmode=opaque'
        tst = 'https://youtu.be/_gWc17vhSAE'
        res = pr.get_embed_youtube(tst)
        eq_(res, exp)

    def test_attribution_unsafe_link(self):
        exp = 'http://www.youtube.com/embed/rSxIk9Qzmmw?enablejsapi=1&wmode=opaque'
        tst = 'http://www.youtube.com/attribution_link?a=gvouc-iy_pw&u=%2Fwatch%3Fv%3DrSxIk9Qzmmw%26feature%3Dshare'
        res = pr.get_embed_youtube(tst)
        eq_(res, exp)

    def test_attribution_safe_link(self):
        exp = 'http://www.youtube.com/embed/rSxIk9Qzmmw?enablejsapi=1&wmode=opaque'
        tst = 'https://www.youtube.com/attribution_link?a=gvouc-iy_pw&u=%2Fwatch%3Fv%3DrSxIk9Qzmmw%26feature%3Dshare'
        res = pr.get_embed_youtube(tst)
        eq_(res, exp)

    def test_ampersand_link(self):
        exp = 'http://www.youtube.com/embed/Zf-YtUuYCDE?enablejsapi=1&wmode=opaque'
        tst = 'https://www.youtube.com/watch?v=Zf-YtUuYCDE#t=289'
        res = pr.get_embed_youtube(tst)
        eq_(res, exp)

    def test_featured_youtube_short(self):
        exp = 'http://www.youtube.com/embed/WtnD8VNEk6c?enablejsapi=1&wmode=opaque'
        tst = 'http://www.youtube.com/watch?v=WtnD8VNEk6c&feature=youtu.be'
        res = pr.get_embed_youtube(tst)
        eq_(res, exp)



class test_get_embed_generic():
    def test_nothing_raises_exception(self):
        assert_raises(AssertionError,pr.get_embed)

    def test_emptystr_raises_exception(self):
        assert_raises(AssertionError,pr.get_embed,"")

    @raises(NotImplementedError)
    def test_provider_NI(self):
        pr.get_embed("http://vimeo.com/caca?bar")

    def test_normal_link(self):
        exp = 'http://www.youtube.com/embed/Xatb2rh3EBw?enablejsapi=1&wmode=opaque'
        tst = 'https://www.youtube.com/watch?v=Xatb2rh3EBw'
        res = pr.get_embed_youtube(tst)
        eq_(res, exp)


# Disabled. Im not sure this is really relevant test.
#    def test_embebed_link(self):
#        tst = 'http://www.youtube.com/embed/P_qPBiBIjP4?enablejsapi=1&wmode=opaque'
#        res = pr.get_embed_youtube(tst)
#        eq_(res, tst)




class test_parse_json_videolisting():
    def test_normal_attachment(self):
        data = { "data":[{u'created_time': 1400579416, u'message': u'Independientemente de si estamos de acuerdo con la cultura arabe o no... \xa1Que preciosos cantos devocionales tienen! \n', u'actor_id': u'642011599209080', u'attachment': {u'media': [{u'src': u'https://fbexternal-a.akamaihd.net/safe_image.php?d=AQAIeVp8w3tE46_Y&w=130&h=130&url=http%3A%2F%2Fi1.ytimg.com%2Fvi%2FWaomfpL7gIU%2Fhqdefault.jpg'}], u'href': u'https://www.youtube.com/watch?v=WaomfpL7gIU&index=4&list=LL-P6qSxOejC1KtbnEQuNtuA', u'name': u'From Srat Al-Kahf by Abo Bakr Shatri', u'description': u'From Srat Al-Kahf by Abo Bakr Shatri'}}
]}
        result = pr.parse_json_video_listing(data)
        eq_(result[0]["preview"] , data["data"][0]["attachment"]["media"][0]["src"])

    def test_empty_src_media(self):
        data = { "data":[{u'created_time': 1400532456, u'message': u'https://www.youtube.com/watch?v=MkYyG1GOETc', u'actor_id': u'10152038751900976', u'attachment': {u'media': [{u'src': u''}], u'href': u'https://www.youtube.com/watch?v=MkYyG1GOETc', u'name': u'The Riptides - 77 Sunset Strip (1979)', u'description': u"Music from Australia and New Zealand in the year 1979: The Riptides' promo-video for the single 'Sunset Strip' (July, 1979). Band Location: Brisbane, QLD, Au..."}}]}
        result = pr.parse_json_video_listing(data)
        eq_("" , data["data"][0]["attachment"]["media"][0]["src"])
        eq_(result[0]["preview"] , "")

    def test_empty_at_all_media(self):
        data = { "data":[{u'created_time': 1400500953, u'message': u'Ha sido una mala semana, con muchas cosas encima, y hoy no he empezado bien el d\xeda, pero me da igual francamente...  https://www.youtube.com/watch?v=y6Sxv-sUYtM :) ',
                          u'actor_id': u'10203087889496668', u'attachment':
                          {u'media': [], u'href':
                           u'https://www.youtube.com/watch?v=y6Sxv-sUYtM',
                           u'name': u'www.youtube.com', u'description': u''}}]}
        result = pr.parse_json_video_listing(data)
        eq_(result[0]["preview"] , "")

