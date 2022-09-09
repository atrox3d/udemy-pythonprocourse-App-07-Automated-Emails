import requests
from pprint import pprint
import datetime
import dateutil.relativedelta

from secret.newsapi_apikey import API_KEY


class NewsFeed:

    def __init__(self, data):
        self.data = data

    def get(self):
        pass


if __name__ == '__main__':
    base_url = 'https://newsapi.org/v2'
    endpoint = 'everything'
    topic = 'cats'

    today = datetime.date.today()                                               # today
    onemonth = dateutil.relativedelta.relativedelta(months=1)                   # +/- 1 month
    from_date = (today - onemonth).isoformat()                                  # 1 month ago YY-mm-dd
    to_date = today.isoformat()                                                 # today YY-mm-dd

    sort_by = 'popularity'
    language = 'en'

    url = (
        f'{base_url}/'
        f'{endpoint}?q='
        f'{topic}&'
        f'from={from_date}&'
        f'to={to_date}&'
        f'sortBy={sort_by}&'
        f'language={language}&'
        f'apiKey={API_KEY}'
        )

    print(f'url: {url}')
    # response = requests.get(url)
    # pprint(response.text)
