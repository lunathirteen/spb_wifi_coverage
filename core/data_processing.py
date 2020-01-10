import pandas as pd
import requests
from pandas.io.json import json_normalize
from sqlalchemy import create_engine
import psycopg2

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


def get_data_from_api(API_HOST, API_TOKEN, dataset_id, write_to=True, **kwargs):

    ApiConnect = APIGovData(API_HOST, API_TOKEN)
    data = ApiConnect.fetch_dataset(str(dataset_id))

    if write_to:
        path = kwargs.get('path', 'data')
        filename = kwargs.get('filename', 'spbwifi.json')
        with open('{}/{}'.format(path, filename), 'w', encoding='utf-8') as f:
            f.write(data + '\n')

    return data

def json2df(json):
    df = json_normalize(eval(json))
    df.columns = df.columns.str.replace('row.', '')
    df = df.drop(['num_id', 'number'], axis=1)
    df = pd.concat([
        df.drop('coordinates', axis=1),
        df['coordinates'].str.split(',', expand=True).add_prefix('coordinate_'
        )], axis=1)

    return df

def df2pg(df, table_name='wifi', drop=True):
    engine = create_engine('postgresql://postgres@db/postgres')
    
    if drop:
        conn_string = "host='db' dbname='postgres' user='postgres'"
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        cursor.execute('drop table if exists wifi')
        cursor.execute('commit')

    df.to_sql(table_name, engine)