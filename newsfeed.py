import requests
from pprint import pprint
import datetime
from dateutil.relativedelta import relativedelta
import json

from secret.newsapi_apikey import API_KEY
from cache import Cache


class NewsFeed:

    def __init__(self, data):
        self.data = data

    def get(self):
        pass


if __name__ == '__main__':
    base_url = 'https://newsapi.org/v2'
    endpoint = 'everything'
    topic = 'cats'

    today = datetime.date.today()                        # today
    onemonth = relativedelta(months=1)                   # +/- 1 month
    from_date = (today - onemonth).isoformat()           # 1 month ago YY-mm-dd
    to_date = today.isoformat()                          # today YY-mm-dd

    sort_by = 'popularity'
    language = 'en'

    url = (                                             # compose url
        f'{base_url}/'                                  # base url
        f'{endpoint}?q='                                # endpoint
        f'{topic}&'                                     # query params
        f'from={from_date}&'                            # TODO: create params from a collection
        f'to={to_date}&'
        f'sortBy={sort_by}&'
        f'language={language}&'
        f'apiKey={API_KEY}'
        )
    print(f'url: {url}')

    cache = Cache(url)
    if USE_CACHE := False:                               # save calls per day
        print(f"using cache: {cache.cachepath}")
        news = cache.load()
    else:
        try:
            request_counter_path = 'files/request-counter.txt'
            with open(request_counter_path, 'r') as fp:
                date = fp.readline().rstrip()
                request_count = fp.readline().rstrip()
                date = datetime.datetime.strptime(date, '%Y-%m-%d')
                request_count = int(request_count)
        except OSError as ose:
            print(ose)
            date = datetime.date.today().isoformat()
            request_count = 0

        print(date, request_count)

        print(f'using requests: {url}')
        # response = requests.get(url)                    # get response
        # news = response.json()                          # get json

        try:
            request_counter_path = 'files/request-counter.txt'
            with open(request_counter_path, 'w') as fp:
                request_count += 1
                date = datetime.date.today().isoformat()
                fp.write(f'{date}\n')
                fp.write(f'{str(request_count)}\n')
        except OSError as ose:
            print(ose)
            exit(1)

    print(date, request_count)
    exit()

    print(type(news))                                   # dict
    # pprint(news, indent=4)                              # pprint json
    cache.save(news)
