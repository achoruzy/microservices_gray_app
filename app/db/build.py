#   Copyright (C) 2021  Arkadiusz Choruzy
#
#   Arkadiusz Choruzy
#   achoruzy@gmail.com

from sqlalchemy import create_engine
import psycopg2
import pandas as pd
import requests
from .schema import metadata

csv_URL = "https://data.cityofnewyork.us/api/views/7yc5-fec2/rows.csv"

db_login = "postgres"  # to aquire from external source when production project
db_password = "postgres"  # to aquire from external source when production project
db_URL = f"postgresql+psycopg2://{db_login}:{db_password}@db:5432/postgres"


def check_csv(url: str) -> bool:
    """Function checks if a CSV file is available.

    Params:
        url (str): an URL link or a filepath to a CSV file

    Returns:
        bool: True if the CSV file is available
    """
    status_code = requests.get(csv_URL).status_code

    if status_code == "200":
        print("CSV status code: 200")
        return True

    print("Can't connect to CSV file.")
    return False


def cleanup_data(csv_dataframe):
    """Function cleans up the data got as csv_dataframe and prepares it
    to be exported into database.

    Params:
        scv_dataframe (pandas.DataFrame): a CSV file parsed to pandas.DataFrame object

    Returns:
        pandas.Dataframe
    """
    df = pd.DataFrame(
        csv_dataframe,
        columns=["School Name", "Category", "Total Enrollment", "%Female", "%Male"],
    )

    return df


def build_db(csv_url: str, db_address: str):
    """Function builds Postgres database with data achived from CSV.

    Params:
        sql_url (str): an URL link or a filepath to a CSV file
    """

    # if not check_csv:
    #     return Exception("CSV file not found")

    # dataset_raw = pd.read_csv(csv_url)

    # dataset_clean = cleanup_data(dataset_raw)

    engine = create_engine(db_address)

    # metadata.create_all(engine)

    # dataset_clean.to_sql("postgres", engine, chunksize=2000)

    return print(f"DB created from CSV file got from: {csv_url}")


def run_db():
    """Function runs database build process."""
    build_db(csv_URL, db_URL)


if __name__ == "__main__":
    pass
