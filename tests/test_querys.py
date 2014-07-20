from nose.tools import assert_raises,eq_,raises,assert_true,ok_,nottest


import friendtube.querys as querys

class test_compose_multiquery():
    @raises(AssertionError)
    def test_none(self):
        """Raises exception if we pass none"""
        eq_(querys.compose_multiquery(None), None)

    def test_two_querys(self):
        """it concatenates 2 querys"""
        q1 = "SELECT uno"
        q2 = "SELECT dos"
        eq_(querys.compose_multiquery([q1,q2]),
            """{"query1":"SELECT uno","query2":"SELECT dos"}"""
           )

    def test_three_querys(self):
        """it concatenates 3 querys"""
        q1 = "SELECT uno"
        q2 = "SELECT dos"
        q3 = "SELECT tres"
        eq_(querys.compose_multiquery([q1,q2,q3]),
            """{"query1":"SELECT uno","query2":"SELECT dos","query3":"SELECT tres"}"""
           )

    def test_print_exapmle(self):
        eq_(querys.fql_multi,False)
