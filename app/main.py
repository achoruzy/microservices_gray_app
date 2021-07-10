#   Copyright (C) 2021  Arkadiusz Choruzy
#
#   Arkadiusz Choruzy
#   achoruzy@gmail.com

from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd

import plotly.express as pex

import schemas, crud
from db import models, database


class Item(BaseModel):
    school_name: str


api = FastAPI()

# -- PLOT --
def plot(data):
    df = pd.DataFrame(data)
    chart = pex.line(data_frame=df)
    return chart.show()


@api.get("/")
def read_root():
    return {"Hello": "Kaszebe"}


@api.get("/filter")
async def filter_data(
    school_name: Optional[str] = None,
    category: Optional[str] = None,
    gender: Optional[str] = None,
    more_than: Optional[int] = None,
    less_than: Optional[int] = None,
):

    with database.SessionLocal() as session:
        data = crud.get_dataset_filtered(
            session, school_name, category, gender, more_than, less_than
        )
    return data


@api.get("/datarow")
async def datarow(id: int):
    with database.SessionLocal() as session:
        data = crud.get_datarow(session, id)
    return data


@api.get("/all_data")
async def all_data():
    with database.SessionLocal() as session:
        data = crud.get_all(session)
    return data
