#   Copyright (C) 2021  Arkadiusz Choruzy
#
#   Arkadiusz Choruzy
#   achoruzy@gmail.com

from sqlalchemy import create_engine


db_URL = "postgresql://postgres:postgres@localhost:5432/postgres"

engine = create_engine(db_URL)
