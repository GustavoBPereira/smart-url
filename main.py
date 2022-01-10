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
    def sanitize_anchor(anchor):
        value = anchor.replace('//', '/').replace(' ', '').replace('#', '')
        return value


class SmartUrl:
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

    def append_query(self, param):
        self.query.update(param)
        return self

    def append_path(self, path):
        self.path = PathUtils(self.path) / path
        return self

    def change_path(self, new_path):
        self.path = PathUtils.sanitize_path(new_path)
        return self

    def change_anchor(self, anchor):
        self.anchor = PathUtils.sanitize_anchor(anchor)
