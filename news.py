import requests
import datetime
import dateutil.relativedelta

from secret.newsapi_apikey import API_KEY
from cache import Cache
from requestcounter import RequestCounter


class NewsFeed:
    """
    """
    base_url = 'https://newsapi.org/v2'
    endpoint = 'everything'
    api_key = API_KEY

    def __init__(
            self,
            interest,
            from_date=None,
            to_date=None,
            language='en',
            sort_by='popularity',
            search_in='title'
    ):
        """

        :param interest:

        :param from_date:   the oldest article allowed,
                            for basic plan: articles up to a month old
                            this is also the default is not specified.
                            -- default if None is yesterday()

        :param to_date: the newest article allowed,
                        for basic plan: New articles available with 1 hour delay
                        this is also the default is not specified
                        -- default if None is today()

        :param language:
        :param sort_by:
        :param search_in:
        """
        self.interest = interest
        self.from_date = self.yesterday() if from_date is None else from_date
        self.to_date = self.today() if to_date is None else to_date
        self.language = language
        self.search_in = search_in
        self.sort_by = sort_by
        self.url = self._composeurl()

        self.cache = Cache()
        self.request_counter = RequestCounter()

    @classmethod
    def today(cls):
        return datetime.datetime.now().strftime('%Y-%m-%d')

    @classmethod
    def yesterday(cls):
        return (
                datetime.datetime.now() -
                datetime.timedelta(days=1)
        ).strftime('%Y-%m-%d')

    @classmethod
    def month(cls):
        return (
                datetime.datetime.now() -
                dateutil.relativedelta.relativedelta(months=1)
        ).strftime('%Y-%m-%d')

    def _composeurl(self):
        # TODO: create params from a collection
        url = (                                                 # compose url
            f'{self.base_url}/'                                 # base url
            f'{self.endpoint}?q='                               # endpoint
            f'{self.interest}&'                                 # query params
            f'searchin={self.search_in}&'
            f'from={self.from_date}&'
            f'to={self.to_date}&'
            f'sortBy={self.sort_by}&'
            f'language={self.language}&'
            f'apiKey={self.api_key}'
        )
        return url

    def get_dict(self, use_cache=True):
        if use_cache:                                           # save free account calls per day
            print(f'NewsFeed | get_dict | using cache')
            news = self.cache.load()                            # load json from cache
        else:
            print(f'NewsFeed | get_dict | using requests')
            response = requests.get(self.url)                   # get response
            news = response.json()                              # get json
            self.request_counter.update()                       # update API calls count per day

        print(f'NewsFeed | get_dict | url | {self.url}')

        self.cache.save(self.url, news)                         # save cache anyway
        return news

    def get_mailbody(self, use_cache=True):
        news = self.get_dict(use_cache)
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

    nf = NewsFeed(
        interest='cats',
        from_date=NewsFeed.month(),
        to_date=NewsFeed.today(),
        language='en'
    )
    print(nf.url)
    mail = nf.get_mailbody()
    print()
    print(mail)
