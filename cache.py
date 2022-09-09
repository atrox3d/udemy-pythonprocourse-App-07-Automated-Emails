import json


class CacheException(Exception):
    pass


class CacheDataMissingException(CacheException):
    pass


class Cache:
    def __init__(
            self,
            cachepath='files/news-cache.json',          # default path
    ):
        self.url = None
        self.cachepath = cachepath
        self.data = None

    def get(self):
        return self.data                                # get data

    def load(self):
        with open(self.cachepath) as fp:                # load data
            self.data = json.load(fp)
        return self.data                                # return data

    def save(self, url, data):
        self.url = url
        self.data = {}                                  # create dict
        self.data.update(data)

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
            raise CacheDataMissingException             # cannot be empty
