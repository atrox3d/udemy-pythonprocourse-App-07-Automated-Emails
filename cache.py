import json


class CacheException(Exception):
    pass


class CacheDataMissingException(CacheException):
    pass


class Cache:
    # cache_filepath = 'files/news-cache.json'
    def __init__(
            self,
            url,
            data=None,
            cachepath='files/news-cache.json',
    ):
        self.url = url
        self.cachepath = cachepath
        self.data = data

    def load(self):
        with open(self.cachepath) as fp:
            self.data = json.load(fp)
        return self.data

    def save(self, data=None):
        self.data = data or self.data

        if self.data:
            with open(self.cachepath, 'w') as fp:       # save json to file news-cache.json

                # https://www.geeksforgeeks.org/python-append-items-at-beginning-of-dictionary/
                url_first = dict(url=self.url)          # try to save url on top of json
                url_first.update(self.data)

                self.data = url_first
                json.dump(
                    self.data,                          # dict
                    fp,                                 # file pointer
                    indent=4                            # pretty print
                )
        else:
            raise CacheDataMissingException

