from unittest import TestCase

from src.smart_url.main import SmartUrl


class SmartUrlTest(TestCase):

    def setUp(self):
        self.url = SmartUrl('https://www.google.com/')

    def test_str(self):
        self.assertEqual('https://www.google.com/', str(self.url))

    def test_str_without_last_slash(self):
        url_without_last_slash = SmartUrl('https://www.google.com')
        self.assertEqual('https://www.google.com/', str(url_without_last_slash))

    def test_host(self):
        self.assertEqual('www.google.com', self.url.host)

    def test_with_port(self):
        url_with_port = SmartUrl('https://www.google.com:1234/')
        self.assertEqual(1234, url_with_port.port)

    def test_without_port(self):
        self.assertEqual(None, self.url.port)

    def test_without_protocol(self):
        url_without_protocol = SmartUrl('www.google.com/')
        self.assertEqual(None, url_without_protocol.protocol)

    def test_with_protocol(self):
        self.assertEqual('https', self.url.protocol)

    def test_secure(self):
        self.assertEqual(True, self.url.is_secure)

    def test_not_secure(self):
        url_not_secure = SmartUrl('http://www.google.com/')
        self.assertEqual(False, url_not_secure.is_secure)

    def test_not_secure_without_protocol(self):
        url_not_secure = SmartUrl('www.google.com/')
        self.assertEqual(False, url_not_secure.is_secure)

    def test_root_path(self):
        self.assertEqual('/', self.url.path)

    def test_root_path_without_last_slash(self):
        url_without_slash = SmartUrl('https://www.google.com')
        self.assertEqual('/', url_without_slash.path)

    def test_path(self):
        url_with_path = SmartUrl('https://www.google.com/path/test/')
        self.assertEqual('/path/test/', url_with_path.path)

    def test_path_special_caracter(self):
        url_with_path = SmartUrl('https://www.google.com/path/test/operação')
        self.assertEqual('/path/test/operação', url_with_path.path)

    def test_path_without_last_slash(self):
        url_with_path = SmartUrl('https://www.google.com/path/test')
        self.assertEqual('/path/test', url_with_path.path)

    def test_append_path(self):
        self.assertEqual('/', self.url.path)
        self.url.append_path('path/test')
        self.assertEqual('/path/test', self.url.path)

    def test_append_path_special_caracter(self):
        self.assertEqual('/', self.url.path)
        self.url.append_path('path/test/operação')
        self.assertEqual('/path/test/operação', self.url.path)

    def test_append_path_remove_double_slash(self):
        self.assertEqual('/', self.url.path)
        self.url.append_path('/path/test')
        self.assertEqual('/path/test', self.url.path)

    def test_change_path(self):
        url = SmartUrl('https://www.google.com/unchanged/path')
        self.assertEqual('/unchanged/path', url.path)
        url.change_path('/changed')
        self.assertEqual('/changed', url.path)

    def test_change_path_without_first_slash(self):
        url = SmartUrl('https://www.google.com/unchanged/path')
        self.assertEqual('/unchanged/path', url.path)
        url.change_path('changed')
        self.assertEqual('/changed', url.path)

    def test_change_path_with_last_slash(self):
        url = SmartUrl('https://www.google.com/unchanged/path')
        self.assertEqual('/unchanged/path', url.path)
        url.change_path('/changed/')
        self.assertEqual('/changed/', url.path)

    def test_without_query(self):
        self.assertEqual({}, self.url.query)

    def test_with_query(self):
        url_with_query = SmartUrl('https://www.google.com/?param=qwe&another_param=123')
        self.assertDictEqual({'param': 'qwe', 'another_param': '123'}, url_with_query.query)

    def test_change_query(self):
        self.assertDictEqual({}, self.url.query)
        self.url.update_query({'test1': '1', 'test2': '2'})
        self.assertDictEqual({'test1': '1', 'test2': '2'}, self.url.query)
        self.url.change_query({'test3': '3'})
        self.assertDictEqual({'test3': '3'}, self.url.query)

    def test_append_param(self):
        self.assertDictEqual({}, self.url.query)
        self.url.update_query({'param':'qwe'})
        self.assertDictEqual({'param':'qwe'}, self.url.query)
        self.url.update_query({'param':'alterated', 'another_param': ['123', '456']})
        self.assertDictEqual({'param':'alterated', 'another_param': ['123', '456']}, self.url.query)

    def test_stacked_append(self):
        self.assertDictEqual({}, self.url.query)
        self.url.update_query({'stacked_call1':'call1'}).update_query({'stacked_call2':'call2'})
        self.assertDictEqual({'stacked_call1': 'call1', 'stacked_call2': 'call2'}, self.url.query)


    def test_anchor(self):
        url = SmartUrl('https://www.google.com/path')
        self.assertEqual('https://www.google.com/path', str(url))
        url.change_anchor('#article-test')
        self.assertEqual('https://www.google.com/path#article-test', str(url))
        url.change_anchor('alterated-anchor-without-sharp')
        self.assertEqual('https://www.google.com/path#alterated-anchor-without-sharp', str(url))