#   Copyright (C) 2021  Arkadiusz Choruzy
#
#   Arkadiusz Choruzy
#   achoruzy@gmail.com

from sqlalchemy import create_engine
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

    # Get desired columns to pd.df
    df = pd.DataFrame(
        csv_dataframe,
        columns=["School Name", "Category", "Total Enrollment", "#Female", "#Male"],
    )

    # Enchance column titles to proper format and to be consistens with db schema
    df.columns = [
        title.lower().replace(" ", "_").replace("#", "") for title in df.columns
    ]

    # Drop rows with NaN, wrong data and reset df indexes
    df = df.dropna(axis=0)
    df.reset_index()

    df = df.drop(
        df[(df.total_enrollment == "s") | (df.female == "s") | (df.male == "s")].index
    )

    datatypes = {
        "school_name": str,
        "category": str,
        "total_enrollment": int,
        "female": int,
        "male": int,
    }

    df = df.astype(datatypes)

    return df


def build_db(csv_url: str, db_address: str):
    """Function builds Postgres database with data achived from CSV.

    Params:
        sql_url (str): an URL link or a filepath to a CSV file
    """

    # Check for CSV file
    if not check_csv:
        return Exception("CSV file not found")

    # Prepare dataset
    dataset_raw = pd.read_csv(csv_url)

    dataset_clean = cleanup_data(dataset_raw)

    print("Dataset cleaned...")

    # Connect to db -> create tables with schema
    engine = create_engine(db_address, echo=False)

    with engine.connect() as con:
        sql_drop_old = "DROP TABLE IF EXISTS school_name, category, total_enrollment, female, male CASCADE;"
        con.execute(sql_drop_old)

    metadata.create_all(engine)

    print("Schema created...")

    # Upload the data to the database
    db_tables = {
        "school": ["school_name"],
        "category": ["category"],
        "school_data": ["total_enrollment", "female", "male"],
    }

    for table_name in db_tables:
        df = pd.DataFrame(dataset_clean, columns=db_tables.get(table_name))

        df.drop_duplicates(inplace=True, ignore_index=True)

        df.to_sql(
            table_name,
            engine,
            if_exists="append",
            index=False,
        )

        print(f"Data imported into <{table_name}> table.")


def run_db():
    """Function runs database build process."""
    build_db(csv_URL, db_URL)

    return print(f"DB created from CSV file got from: {csv_URL}")


if __name__ == "__main__":
    pass
