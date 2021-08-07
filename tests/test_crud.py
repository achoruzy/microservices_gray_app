#   Copyright (C) 2021  Arkadiusz Choruzy
#
#   Arkadiusz Choruzy
#   achoruzy@gmail.com


# -- INTERNAL IMPORTS --
from app import crud
from app.db import database


def test_get_datarow():
    json_resp = {'total_enrollment': 162,
                 'id': 1,
                 'school_name': "P.S. 015 Roberto Clemente",
                 'male': 83,
                 'female': 79,
                 'category': "All Students"}

    with database.SessionLocal() as session:
        data = crud.get_datarow(session, 1)

        assert data == json_resp
