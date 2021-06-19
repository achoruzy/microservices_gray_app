#   Copyright (C) 2021  Arkadiusz Choruzy
#
#   Arkadiusz Choruzy
#   achoruzy@gmail.com

from sqlalchemy import create_engine
import pandas as pd
import requests
import schema

csv_URL = 'https://data.cityofnewyork.us/api/views/7yc5-fec2/rows.csv'

db_login = 'postgres'  # to aquire from external source when production project
db_password = 'postgres'  # to aquire from external source when production project
db_URL = f'postgresql://{db_login}:{db_password}@localhost:5432/postgres'


def check_csv(url: str) -> bool:
    '''Function checks if a CSV file is available.

    Params:
        url (str): an URL link or a filepath to a CSV file

    Returns:
        bool: True if the CSV file is available
    '''
    status_code = requests.get(csv_URL).status_code

    if status_code == '200':
        return True
    return False


def cleanup_data(csv_dataframe):
    '''Function cleans up the data got as csv_dataframe and prepares it
    to be exported into database.

    Params:
        scv_dataframe (pandas.DataFrame): a CSV file parsed to pandas.DataFrame object

    Returns:
        pandas.Dataframe
    '''
    df = pd.DataFrame(csv_dataframe, columns=[
                      'School Name', 'Category', 'Total Enrollment', '%Female', '%Male'])

    return df


def build_db(url):
    '''Function exports data achived from CSV to PostgreSQL database.
    '''

    if not check_csv:
        return Exception('CSV file not found')

    dataset_raw = pd.read_sql(url)

    dataset_clean = cleanup_data(dataset_raw)

    engine = create_engine(db_URL)

    schema.metadata.create_all(engine)


if __name__ == '__main__':
    build_db()
