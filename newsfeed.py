import requests
from pprint import pprint
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
    from_date = '2022-08-10'
    to_date = '2022-09-08'
    sort_by = 'popularity'

    url = (f'{base_url}/'
           f'{endpoint}?q='
           f'{topic}&'
           f'from={to_date}&'
           # f'to={to_date}&'
           f'sortBy={sort_by}&'
           f'apiKey={API_KEY}'
           )

    print(f'url: {url}')
    response = requests.get(url)
    pprint(response.text)
