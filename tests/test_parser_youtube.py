#!/usr/bin/env python

from nose.tools import assert_raises,eq_,raises,assert_true,ok_,nottest
from mock import Mock, MagicMock, patch

import friendtube.parse_youtube as pr
class test_get_embed_youtube():
    def test_nothing_raises_exception(self):
        assert_raises(AssertionError,pr.get_embed_youtube)

    def test_emptystr_raises_exception(self):
        assert_raises(AssertionError,pr.get_embed_youtube,"")

    def test_mixed_link(self):
        tst="https://www.youtube.com/watch?v=18NmQEA5lzo&feature=youtu.be"
        exp="https://www.youtube.com/embed/18NmQEA5lzo?enablejsapi=1&wmode=opaque"
        res = pr.get_embed_youtube(tst)
        eq_(res, exp)

    @raises(NotImplementedError)
    def test_malformed_link(self):
        pr.get_embed_youtube("youtu.be/caca?bar")

    def test_normal_link(self):
        exp = 'https://www.youtube.com/embed/Xatb2rh3EBw?enablejsapi=1&wmode=opaque'
        tst = 'https://www.youtube.com/watch?v=Xatb2rh3EBw'
        res = pr.get_embed_youtube(tst)
        eq_(res, exp)

    def test_dirty_link(self):
        exp = 'https://www.youtube.com/embed/dBwMQAaLUoY?enablejsapi=1&wmode=opaque'
        tst = 'http://www.youtube.com/watch?v=dBwMQAaLUoY&feature=player_embedded'
        res = pr.get_embed_youtube(tst)
        eq_(res, exp)

    def test_short_unsafe_link(self):
        exp = 'https://www.youtube.com/embed/_gWc17vhSAE?enablejsapi=1&wmode=opaque'
        tst = 'http://youtu.be/_gWc17vhSAE'
        res = pr.get_embed_youtube(tst)
        eq_(res, exp)

    def test_short_safe_link(self):
        exp = 'https://www.youtube.com/embed/_gWc17vhSAE?enablejsapi=1&wmode=opaque'
        tst = 'https://youtu.be/_gWc17vhSAE'
        res = pr.get_embed_youtube(tst)
        eq_(res, exp)

    def test_attribution_unsafe_link(self):
        exp = 'https://www.youtube.com/embed/rSxIk9Qzmmw?enablejsapi=1&wmode=opaque'
        tst = 'http://www.youtube.com/attribution_link?a=gvouc-iy_pw&u=%2Fwatch%3Fv%3DrSxIk9Qzmmw%26feature%3Dshare'
        res = pr.get_embed_youtube(tst)
        eq_(res, exp)

    @raises(NotImplementedError)
    def test_attribution_another_link(self):
        exp = 'https://www.youtube.com/embed/?enablejsapi=1&wmode=opaque'
        tst = 'http://www.youtube.com/attribution_link?a=xQgZSJGi75Q&u=%2Fplaylist%3Flist%3DPLF72C3E0A45E3093C'
        res = pr.get_embed_youtube(tst)
        eq_(res, exp)

    def test_attribution_safe_link(self):
        exp = 'https://www.youtube.com/embed/rSxIk9Qzmmw?enablejsapi=1&wmode=opaque'
        tst = 'https://www.youtube.com/attribution_link?a=gvouc-iy_pw&u=%2Fwatch%3Fv%3DrSxIk9Qzmmw%26feature%3Dshare'
        res = pr.get_embed_youtube(tst)
        eq_(res, exp)

    def test_ampersand_link(self):
        exp = 'https://www.youtube.com/embed/Zf-YtUuYCDE?enablejsapi=1&wmode=opaque'
        tst = 'https://www.youtube.com/watch?v=Zf-YtUuYCDE#t=289'
        res = pr.get_embed_youtube(tst)
        eq_(res, exp)

    def test_featured_youtube_short(self):
        exp = 'https://www.youtube.com/embed/WtnD8VNEk6c?enablejsapi=1&wmode=opaque'
        tst = 'http://www.youtube.com/watch?v=WtnD8VNEk6c&feature=youtu.be'
        res = pr.get_embed_youtube(tst)
        eq_(res, exp)

    def test_reversed_order_featured(self):
        exp = 'https://www.youtube.com/embed/xTiF7Hk8NAU?enablejsapi=1&wmode=opaque'
        tst = 'https://www.youtube.com/watch?feature=player_embedded&v=xTiF7Hk8NAU'
        res = pr.get_embed_youtube(tst)
        eq_(res, exp)



