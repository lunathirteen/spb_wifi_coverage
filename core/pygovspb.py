import requests
import json


class APIGovData():
    """"""
    def __init__(self, host, token):
        self.host = host
        self.token = token
    def _params(self, page=None, per_page=1000):

        params = {'per_page': per_page}
        if page:
            params.get('page', page)

        return params

    def fetch_dataset(self, dataset_id):
        url = self.host + '/api/v1/datasets/{}/versions/latest/data'.format(dataset_id)
        headers = {'Authorization': 'Token {}'.format(self.token)}
        params = self._params()

        result = requests.get(url, headers=headers, params=params)
        return result.text


if __name__ == "__main__":
    API_HOST = 'http://data.gov.spb.ru'
    API_TOKEN = 'changeme'
    
    ApiConnect = APIGovData(API_HOST, API_TOKEN)
    data = ApiConnect.fetch_dataset('29')
    with open('data/spbwifi.json', 'w', encoding='utf-8') as f:
        f.write(data + '\n')
