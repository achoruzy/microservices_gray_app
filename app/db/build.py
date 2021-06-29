#   Copyright (C) 2021  Arkadiusz Choruzy
#
#   Arkadiusz Choruzy
#   achoruzy@gmail.com

from sqlalchemy import create_engine, MetaData
import pandas as pd
import requests
from .schema import metadata

csv_URL = "https://data.cityofnewyork.us/api/views/7yc5-fec2/rows.csv"

db_login = "postgres"  # to aquire from external source when production project
db_password = "postgres"  # to aquire from external source when production project
db_URL = f"postgresql+psycopg2://{db_login}:{db_password}@db:5432/postgres"

TABLE = "school_data"
COLUMNS = {
    "School Name": str,
    "Category": str,
    "Total Enrollment": int,
    "#Female": int,
    "#Male": int,
}


def check_csv(url: str) -> bool:
    """Function checks if the CSV file is available.

    Params:
        url (str): an URL link or a filepath to a CSV file

    Returns:
        bool: True if the CSV file is available
    """
    status_code = requests.get(csv_URL).status_code

    if status_code == "200":
        print("CSV status code: 200")
        return True

    print("Error: Can't connect to CSV file.")
    return False


def cleanup_data(csv_dataframe, columns: dict = COLUMNS):
    """Function cleans up the data got as csv_dataframe and prepares it
    to be exported into database.

    Params:
        scv_dataframe (pandas.DataFrame): a CSV file parsed to pandas.DataFrame object
        columns (dict: {str: type}): a dictiodnary in type {"column name from csv_dataframe": wanted datatype}

    Returns:
        pandas.Dataframe
    """
    # Get desired columns to pd.df
    df = pd.DataFrame(
        csv_dataframe,
        columns=columns,
    )

    # Enchance column titles to proper format and to be consistens with db schema
    df.columns = [
        title.lower().replace(" ", "_").replace("#", "") for title in df.columns
    ]

    # Drop rows with NaN or wrong data
    df = df.dropna(axis=0)
    df = df.drop(
        df[(df.total_enrollment == "s") | (df.female == "s") | (df.male == "s")].index
    )

    # Set datatypes for columns
    datatypes = {
        col.lower().replace(" ", "_").replace("#", ""): typ
        for (col, typ) in columns.items()
    }
    df = df.astype(datatypes)

    return df


def build_db(csv_url: str = csv_URL, db_address: str = db_URL):
    """Function builds Postgres database with data achived from CSV.

    Params:
        sql_url (str): an URL link or a filepath to a CSV file
        db_address (str): a database host address to connect
    """

    # Check for CSV file
    if not check_csv:
        return Exception("CSV file not found")

    # Prepare dataset to match db schema
    dataset_raw = pd.read_csv(csv_url)
    dataset_clean = cleanup_data(dataset_raw)
    print("Dataset cleaned...")

    # Connection to db
    engine = create_engine(db_address, echo=False)
    print("DB connection established...")

    # Drop schema tables
    meta = MetaData(engine)
    meta.reflect()
    meta.drop_all()
    print("Schema dropped...")

    # Create new db tables with schema
    metadata.create_all(engine)
    print("Schema created...")

    # Import the data to the database
    table = list(meta.tables.keys())[0]

    dataset_clean.to_sql(
        table,
        engine,
        if_exists="append",
        index=False,
    )
    print(f"Fresh data imported into <{table}> table.")
    print(f"DB created from CSV file downloaded from: {csv_URL}")

    return


if __name__ == "__main__":
    pass
