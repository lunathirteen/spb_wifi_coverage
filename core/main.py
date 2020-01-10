import sys
from core import data_processing as dp


def main(host, token, dataset_id):

    json_data = dp.get_data_from_api(host, token, dataset_id)

    df = dp.json2df(json_data)

    dp.df2pg(df, 'wifi')

if __name__ == "__main__":
    API_HOST = sys.argv[1]
    API_TOKEN = sys.argv[2]

    main(API_HOST, API_TOKEN, dataset_id=29)