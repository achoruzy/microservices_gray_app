#   Copyright (C) 2021  Arkadiusz Choruzy
#
#   Arkadiusz Choruzy
#   achoruzy@gmail.com

from fastapi.testclient import TestClient

# -- INTERNAL IMPORTS --
from app.main import api

client = TestClient(api)


def test_datarow():
    response = client.get("/datarow?id=1")

    json_resp = {'total_enrollment': 162,
                 'id': 1,
                 'school_name': "P.S. 015 Roberto Clemente",
                 'male': 83,
                 'female': 79,
                 'category': "All Students"}

    assert response.status_code == 200
    assert response.json() == json_resp
