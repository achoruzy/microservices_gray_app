#   Copyright (C) 2021  Arkadiusz Choruzy
#
#   Arkadiusz Choruzy
#   achoruzy@gmail.com

# -- FOR TEST IMPORT --
from app.db import build

import pandas as pd


def test_check_csv():
    # CASE A
    url_a = 'https://mock.codes/400'
    result_a = build.check_csv(url_a)
    assert result_a == False
    # CASE B
    url_b = 'https://mock.codes/200'
    result_b = build.check_csv(url_b)
    assert result_b == True


def test_cleanup_data():
    dataset = {'School Name': ['P.S. 015 Roberto Clemente'],
               'Category': ['All Students'],
               'Total Enrollment': ['162'],
               '#Female': ['79'],
               '#Male': ['83']
               }

    columns = {
        "School Name": str,
        "Category": str,
        "Total Enrollment": int,
        "#Female": int,
        "#Male": int,
    }

    csv_data = pd.DataFrame.from_dict(
        data=dataset)

    result = build.cleanup_data(csv_data, columns)

    assert list(result.columns.values) == [
        'school_name', 'category', 'total_enrollment', 'female', 'male']
