import requests
from pprint import pprint
import datetime
from dateutil.relativedelta import relativedelta
import json

from secret.newsapi_apikey import API_KEY
from cache import Cache
from requestcounter import RequestCounter


class NewsFeed:

    def __init__(self, data):
        self.data = data

    def get(self):
        pass


if __name__ == '__main__':
    base_url = 'https://newsapi.org/v2'
    endpoint = 'everything'
    topic = 'cats'

    # TODO: check date format
    today = datetime.date.today()                        # today
    onemonth = relativedelta(months=1)                   # +/- 1 month
    from_date = (today - onemonth).isoformat()           # 1 month ago YY-mm-dd
    to_date = today.isoformat()                          # today YY-mm-dd

    sort_by = 'popularity'
    language = 'en'

    # TODO: create params from a collection
    url = (                                             # compose url
        f'{base_url}/'                                  # base url
        f'{endpoint}?q='                                # endpoint
        f'{topic}&'                                     # query params
        f'from={from_date}&'                            
        f'to={to_date}&'
        f'sortBy={sort_by}&'
        f'language={language}&'
        f'apiKey={API_KEY}'
        )
    print(f'url: {url}')

    cache = Cache()
    if USE_CACHE := True:                               # save calls per day
        print(f"using cache: {cache.cachepath}")
        news = cache.load()
    else:
        rc = RequestCounter()
        print(rc.date, rc.count)

        print(f'using requests: {url}')
        response = requests.get(url)                    # get response
        news = response.json()                          # get json

        rc.update()
        print(rc.date, rc.count)

    print(type(news))                                   # dict
    # pprint(news, indent=4)                              # pprint json
    cache.save(url, news)
