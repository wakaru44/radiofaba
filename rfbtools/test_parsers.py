from nose.tools import assert_raises,eq_,raises,assert_true,ok_

import rfbtools.parsers as pr

class test_get_embed_youtube():
    def test_nothing_raises_exception(self):
        assert_raises(AssertionError,pr.get_embed_youtube)

    def test_emptystr_raises_exception(self):
        assert_raises(AssertionError,pr.get_embed_youtube,"")

    def test_malformed_link(self):
        res = pr.get_embed_youtube("youtu.be/caca?bar")
        ok_(res)

# Disabled. Im not sure this is really relevant test.
#    def test_embebed_link(self):
#        tst = 'http://www.youtube.com/embed/P_qPBiBIjP4?enablejsapi=1&wmode=opaque'
#        res = pr.get_embed_youtube(tst)
#        eq_(res, tst)

    def test_normal_link(self):
        exp = 'http://www.youtube.com/embed/Xatb2rh3EBw?enablejsapi=1&wmode=opaque'
        tst = 'https://www.youtube.com/watch?v=Xatb2rh3EBw'
        res = pr.get_embed_youtube(tst)
        eq_(res, exp)



class test_get_embed_regular():
    def test_nothing_raises_exception(self):
        assert_raises(AssertionError,pr.get_embed)

    def test_emptystr_raises_exception(self):
        assert_raises(AssertionError,pr.get_embed,"")

    def test_malformed_link(self):
        res = pr.get_embed("youtu.be/caca?bar")
        ok_(res)

# Disabled. Im not sure this is really relevant test.
#    def test_embebed_link(self):
#        tst = 'http://www.youtube.com/embed/P_qPBiBIjP4?enablejsapi=1&wmode=opaque'
#        res = pr.get_embed_youtube(tst)
#        eq_(res, tst)

    def test_normal_link(self):
        exp = 'http://www.youtube.com/embed/Xatb2rh3EBw?enablejsapi=1&wmode=opaque'
        tst = 'https://www.youtube.com/watch?v=Xatb2rh3EBw'
        res = pr.get_embed(tst)
        eq_(res, exp)

    def test_dirty_link(self):
        exp = 'http://www.youtube.com/embed/dBwMQAaLUoY?enablejsapi=1&wmode=opaque'
        tst = 'http://www.youtube.com/watch?v=dBwMQAaLUoY&feature=player_embedded'
        res = pr.get_embed(tst)
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


