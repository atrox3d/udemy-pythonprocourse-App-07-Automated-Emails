import requests
import datetime
from dateutil.relativedelta import relativedelta

from secret.newsapi_apikey import API_KEY
from cache import Cache
from requestcounter import RequestCounter


class NewsFeed:
    """
    """
    base_url = 'https://newsapi.org/v2'
    endpoint = 'everything'
    api_key = API_KEY

    def __init__(self, interest, from_date, to_date, language, sort_by='popularity', search_in='title'):
        self.interest = interest
        self.from_date = from_date
        self.to_date = to_date
        self.language = language
        self.search_in = search_in
        self.sort_by = sort_by
        self.url = self._composeurl()

        self.cache = Cache()
        self.request_counter = RequestCounter()

    def _composeurl(self):
        # TODO: create params from a collection
        url = (                                         # compose url
            f'{self.base_url}/'                         # base url
            f'{self.endpoint}?q='                       # endpoint
            f'{self.interest}&'                         # query params
            f'searchin={self.search_in}&'
            f'from={self.from_date}&'
            f'to={self.to_date}&'
            f'sortBy={self.sort_by}&'
            f'language={self.language}&'
            f'apiKey={self.api_key}'
        )
        return url

    def _get(self, use_cache=True):
        if use_cache:                                   # save free account calls per day
            news = self.cache.load()                    # load json from cache
        else:
            print(f'using requests: {self.url}')
            response = requests.get(self.url)           # get response
            news = response.json()                      # get json
            self.request_counter.update()               # update API calls count per day

        print(type(news))  # dict

        self.cache.save(self.url, news)                 # save cache anyway
        return news

    def get(self, use_cache=True):
        news = self._get(use_cache)
        articles = news['articles']
        email_body = ''

        for article in articles:
            email_body += f'{article["title"]}\n'
            email_body += f'{article["url"]}\n'
            email_body += f'\n'

        return email_body


if __name__ == '__main__':
    # TODO: check date format
    today = datetime.date.today()  # today
    onemonth = relativedelta(months=1)  # +/- 1 month
    from_date = (today - onemonth).isoformat()  # 1 month ago YY-mm-dd
    to_date = today.isoformat()  # today YY-mm-dd

    nf = NewsFeed(
        interest='cats',
        from_date=from_date,
        to_date=to_date,
        language='en'
    )
    print(nf.url)
    mail = nf.get()
    print()
    print(mail)

