#   Copyright (C) 2021  Arkadiusz Choruzy
#
#   Arkadiusz Choruzy
#   achoruzy@gmail.com

import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv, find_dotenv

# Get environment variables from .env file
load_dotenv(find_dotenv())

# Dataset for consideration - data got from used CSV data file
TABLE = "school_data"
COLUMNS = {
    "School Name": str,
    "Category": str,
    "Total Enrollment": int,
    "#Female": int,
    "#Male": int,
}


# PostgreSQL database access credentials
DB_ADDRESS = "db:5432"
DB_LOGIN = os.getenv("DB_LOGIN")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_TITLE = os.getenv("DB_TITLE")
DB_URL = f"postgresql+psycopg2://{DB_LOGIN}:{DB_PASSWORD}@{DB_ADDRESS}/{DB_TITLE}"


# DB connections
engine = create_engine(DB_URL, echo=False)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()
