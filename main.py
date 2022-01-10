import re
from urllib.parse import urlparse, urlunparse, urlencode, parse_qsl



class PathUtils(str):
    def __truediv__(self, other):
        """Soma os caminhos relativos considerando os separadores"""
        if self.endswith('/'):
            value = self + other.lstrip('/')
        elif other.startswith('/'):
            value = self + other
        else:
            value = self + '/' + other
        return self.__class__(self.sanitize_path(value))

    @staticmethod
    def sanitize_path(path):
        value = path.replace('//', '/').replace(' ', '')
        if not value.startswith('/'):
            value = f'/{value}'
        return value

    @staticmethod
    def sanitize_anchor(anchor, with_sharp=False):
        value = anchor.replace('//', '/').replace(' ', '').replace('#', '')
        if value and with_sharp and not value.startswith('#'):
            value = f'#{value}'
        return value

    @staticmethod
    def sanitize_query(query):
        if not query:
            return ''
        value = query.replace(' ', '')
        if not value.startswith('?'):
            value = f'?{value}'
        return value


class SmartPath:
    use_sharp_in_anchor = True

    def __init__(self, path, query=None, anchor=''):
        if query is None:
            self.query = {}
        else:
            self.query = query
        self.path = PathUtils.sanitize_path(path)
        self.anchor = PathUtils.sanitize_anchor(anchor, with_sharp=True)

    def __str__(self):
        query = PathUtils.sanitize_query(urlencode(self.query))
        return f"{self.path if self.path else '/'}{query}{self.anchor}"

    def update_query(self, param):
        self.query.update(param)
        return self

    def append_path(self, path):
        self.path = PathUtils(self.path) / path
        return self

    def change_path(self, new_path):
        self.path = PathUtils.sanitize_path(new_path)
        return self

    def change_anchor(self, anchor):
        self.anchor = PathUtils.sanitize_anchor(anchor, with_sharp=self.use_sharp_in_anchor)


class SmartUrl(SmartPath):
    use_sharp_in_anchor = False

    def __init__(self, url):
        parsed_url = urlparse(url)
        self.host = parsed_url.hostname
        self.port = parsed_url.port
        self.protocol = parsed_url.scheme if parsed_url.scheme else None
        self.is_secure = bool(re.match(r"(https|wss)", self.protocol)) if self.protocol else False
        self.path = parsed_url.path if parsed_url.path else '/'
        self.query = dict(parse_qsl(parsed_url.query))

        self.netloc = parsed_url.netloc
        self.anchor = parsed_url.fragment

    def __str__(self):
        return urlunparse([self.protocol, self.netloc, self.path, None, urlencode(self.query, encoding='utf-8'), self.anchor])
