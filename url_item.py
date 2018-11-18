class UrlItem(object):
    def __init__(self, url, depth=0):
        self.url = url
        self.depth = depth
    def __eq__(self, other):
        if isinstance(other, UrlItem):
            return self.url == other.url and self.depth == other.depth
        return object.__eq__(self, other)

