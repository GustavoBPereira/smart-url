from unittest import TestCase
from main import SmartPath


class SmartUrlTest(TestCase):

    def setUp(self):
        self.path = SmartPath('/path/test')

    def test_str(self):
        self.assertEqual('/path/test', str(self.path))

    def test_change_path(self):
        self.path.change_path('new_path')
        self.assertEqual('/new_path', str(self.path))

    def test_append_path(self):
        self.path.append_path('new_path')
        self.assertEqual('/path/test/new_path', str(self.path))
        self.path.append_path('/with_slash')
        self.assertEqual('/path/test/new_path/with_slash', str(self.path))

    def test_query(self):
        self.path = SmartPath('/path/test', query={'test': 'qwe'})
        self.assertEqual('/path/test?test=qwe', str(self.path))

    def test_append_query(self):
        self.path = SmartPath('/path/test', query={'test': 'qwe'})
        self.path.append_query({'new_test': '123'})
        self.assertEqual('/path/test?test=qwe&new_test=123', str(self.path))


    def test_anchor(self):
        self.path = SmartPath('/path/test', anchor='article-1')
        self.assertEqual('/path/test#article-1', str(self.path))

    def test_change_anchor(self):
        self.path = SmartPath('/path/test', anchor='article-1')
        self.assertEqual('/path/test#article-1', str(self.path))
        self.path.change_anchor('test-edit-anchor')
        self.assertEqual('/path/test#test-edit-anchor', str(self.path))