import json

import luigi
import pandas as pd
import requests
from pandas.io.json import json_normalize
from luigi.contrib.postgres import PostgresTarget
from sqlalchemy import create_engine

import psycopg2


class DownloadDataset(luigi.Task):

    def run(self):

        headers = {
            'Authorization': 'Token 1380b98f2394286238e3b36be5336015d2a11ca9'
            }

        params = {'per_page': 1000}
        url = 'http://data.gov.spb.ru/api/v1/datasets/29/versions/latest/data/'

        result_dataset = requests.get(
            url=url,
            headers=headers,
            params=params)

        self.output().makedirs()
        with open('./data/spbwifi.json', 'w', encoding='utf-8') as f:
            f.write(result_dataset.text + '\n')

    def output(self):
        return luigi.LocalTarget('./data/spbwifi.json')


class TransformDataset(luigi.Task):
    def requires(self):
        return DownloadDataset()

    def run(self):

        with open(self.input().path) as json_file:
            json_data = json.load(json_file)

        df = json_normalize(json_data)
        df.columns = df.columns.str.replace('row.', '')
        df = df.drop(['num_id', 'number'], axis=1)
        df = pd.concat([
            df.drop('coordinates', axis=1),
            df['coordinates'].str.split(',', expand=True)
            .add_prefix('coordinate_')
            ], axis=1)

        df.to_csv(self.output().path)

    def output(self):
        return luigi.LocalTarget('./data/spbwifi.csv')


class LoadDatasetPostgres(luigi.Task):
    def requires(self):
        return TransformDataset()

    def run(self):

        engine = create_engine('postgresql://postgres@db/postgres')

        conn_string = "host='db' dbname='postgres' user='postgres'"
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        cursor.execute('drop table if exists wifi')
        cursor.execute('commit')

        df = pd.read_csv(self.input().path)
        df.to_sql('wifi', engine)

    def output(self):
        return PostgresTarget(
            host='db',
            database='postgres',
            user='postgres',
            password='',
            table='wifi',
            update_id='wifi')


if __name__ == "__main__":
    luigi.run()
