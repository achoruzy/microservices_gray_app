#   Copyright (C) 2021  Arkadiusz Choruzy
#
#   Arkadiusz Choruzy
#   achoruzy@gmail.com

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Dataset
TABLE = "school_data"
COLUMNS = {
    "School Name": str,
    "Category": str,
    "Total Enrollment": int,
    "#Female": int,
    "#Male": int,
}


# Database Postgresql
DB_LOGIN = "postgres"  # to aquire from external source when production project
DB_PASSWORD = "postgres"  # to aquire from external source when production project
DB_TITLE = "postgres"
DB_URL = f"postgresql+psycopg2://{DB_LOGIN}:{DB_PASSWORD}@db:5432/{DB_TITLE}"


engine = create_engine(DB_URL, echo=False)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()
