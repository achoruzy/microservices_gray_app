#   Copyright (C) 2021  Arkadiusz Choruzy
#
#   Arkadiusz Choruzy
#   achoruzy@gmail.com

from sqlalchemy.orm import Session


# -- INTERNAL IMPORTS --
from app import crud
from app.db import database, models


def test_get_datarow():
    resp = {'total_enrollment': 162,
            'id': 1,
            'school_name': "P.S. 015 Roberto Clemente",
            'male': 83,
            'female': 79,
            'category': "All Students"}

    with database.SessionLocal() as session:
        data = crud.get_datarow(session, 1)

        assert type(data) == models.Data
        assert data.male == resp['male']
        assert data.category == resp['category']
