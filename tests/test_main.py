#   Copyright (C) 2021  Arkadiusz Choruzy
#
#   Arkadiusz Choruzy
#   achoruzy@gmail.com

from fastapi.testclient import TestClient
import pandas as pd


# -- INTERNAL IMPORTS --
from app import main
from app.main import api
from app.db import database

client = TestClient(api)


def test_datarow():
    # Unit test is also responsible for testing main.all_data and database connection availability
    response = client.get("/datarow?id=1")

    json_resp = {'total_enrollment': 162,
                 'id': 1,
                 'school_name': "P.S. 015 Roberto Clemente",
                 'male': 83,
                 'female': 79,
                 'category': "All Students"}

    assert response.status_code == 200
    assert response.json() == json_resp


def test_read_root():
    response = client.get("/")

    assert response.status_code == 200


def test_query_to_df():
    with database.SessionLocal() as session:
        data = main.query_to_df(session)

        assert type(data) == pd.DataFrame
