import requests
import json


class GovData():
    """"""
    def __init__(self, host, token):
        self.host = host
        self.token = token

    def fetch_dataset(self, dataset_id):
        url = self.host + '/api/v1/datasets/{}/versions/latest/data'.format(dataset_id)
        headers = {'Authorization': 'Token {}'.format(self.token)}
        params = {'per_page': '1000'}

        result = requests.get(url, headers=headers, params=params)
        return result.text

"""
    headers = {'Authorization':'Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b'}
    result = requests.get('http://data.gov.spb.ru/api/v1/datasets/18/', headers=headers)
    result.text
"""

if __name__ == "__main__":
    API_HOST = 'http://data.gov.spb.ru'
    API_TOKEN = 'changeme'
    
    ApiConnect = GovData(API_HOST, API_TOKEN)
    data = ApiConnect.fetch_dataset('29')
    with open('data/spbwifi.json', 'w', encoding='utf-8') as f:
        f.write(data + '\n')