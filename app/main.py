#   Copyright (C) 2021  Arkadiusz Choruzy
#
#   Arkadiusz Choruzy
#   achoruzy@gmail.com

from typing import Optional
import dataclasses

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from pydantic import BaseModel
import pandas as pd

import plotly.express as pex
import plotly.offline as pof

import schemas
import crud
from db import models, database

from worker import celery


class Item(BaseModel):
    school_name: str


api = FastAPI()


# -- PLOT CHART FUNCTION --
def query_to_df(data):
    df = pd.DataFrame()
    for row in data:
        del row.__dict__["_sa_instance_state"]
        del row.__dict__["id"]
        df = df.append(row.__dict__, ignore_index=True)
    return df


def plot_chart(data):
    df = query_to_df(data)
    chart = pex.bar(df,
                    x="school_name",
                    y="total_enrollment",
                    title="New York Secondary Schools",
                    labels={"school_name": "School name",
                            "total_enrollment": "Total enrollment"},
                    text="total_enrollment",
                    color="total_enrollment",
                    color_continuous_scale="teal",
                    )

    return pof.plot(chart, output_type="div")


# -- REST FUNCTIONS --


@api.get("/")
def read_root():
    return {"Hello": "github"}


@api.get("/filter", response_class=HTMLResponse)
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

    html_content = plot_chart(data)

    return HTMLResponse(content=html_content, status_code=200)


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
