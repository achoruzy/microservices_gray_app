#   Copyright (C) 2021  Arkadiusz Choruzy
#
#   Arkadiusz Choruzy
#   achoruzy@gmail.com

from typing import Optional

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import pandas as pd

import plotly.express as pex
import plotly.offline as pof

from sqlalchemy.orm import Session

# -- INTERNAL IMPORTS --
import app.crud as crud
from app.db import models, database
from app.worker import celery


# -- PLOT CHART FUNCTIONS --

def query_to_df(data: Session.query) -> pd.DataFrame:
    """
    Translates SQLAlchemy query to pandas dataframe with data clean-up.

    Args:
        data: sqlalchemy.orm.Session.query - SQL dataset got by query

    Returns:
        pandas.Dataframe
    """
    df = pd.DataFrame()

    for row in data:
        # query data rows as below has to be removed for proper usage
        del row.__dict__["_sa_instance_state"]
        del row.__dict__["id"]
        df = df.append(row.__dict__, ignore_index=True)

    return df


@celery.task(serializer='pickle')
def plot_chart(data: Session.query) -> str:
    """
    Asynchronised function for chart generation from given data.

    Args:
        data: sqlalchemy.orm.Session.query - SQL dataset got by query

    Returns:
        str - chart for data taken as HTML/CSS/js code
    """
    df = query_to_df(data)

    # PLOTLY CHART
    chart = pex.bar(df,
                    x="school_name",
                    y="total_enrollment",
                    title="New York Secondary Schools",
                    labels={"school_name": "School name",
                            "total_enrollment": "Total enrollment"},
                    text="total_enrollment",
                    color="total_enrollment",
                    color_continuous_scale="teal_r",
                    template="plotly_dark",
                    opacity=0.7
                    )

    # ADD MEAN LINE
    average = int(df.mean(axis=0)[2])

    chart.add_shape(type="line",
                    line_color="lightsalmon",
                    line_width=2, opacity=1,
                    line_dash="dash",
                    x0=0, x1=1, xref="paper",
                    y0=average, y1=average, yref="y"
                    )

    result_html = pof.plot(chart, output_type="div")

    return result_html


# -- REST API --

api = FastAPI()

api.mount("/static",
          StaticFiles(directory="static",
                      name="static"
                      ))


@api.get("/", response_class=HTMLResponse)
def read_root():
    """ Endpoint returns root page for the service.
    """

    template = r"<html>Hi there!</html>"

    return HTMLResponse(content=template, status_code=200)


@api.get("/filter", response_class=HTMLResponse)
async def filter_data(
    school_name: Optional[str] = None,
    category: Optional[str] = None,
    gender: Optional[str] = None,
    more_than: Optional[int] = None,
    less_than: Optional[int] = None,
):
    """ Endpoint returns plotly chart for filtered data.

        Filters:
            school_name - as in data
            category - as in data
            gender - all, female, male
            more_than - specify a number for gender
            less_than - specify a number for gender
    """

    with database.SessionLocal() as session:
        data = crud.get_dataset_filtered(
            session, school_name, category, gender, more_than, less_than
        )

    html_content = plot_chart.delay(data)

    return HTMLResponse(content=html_content.get(), status_code=200)


@api.get("/datarow")
async def datarow(id: int):
    """ Endpoint returns json data of specified row id from database.
    """
    with database.SessionLocal() as session:
        data = crud.get_datarow(session, id)

    return data


@api.get("/all_data")
async def all_data():
    """ Endpoint returns json data for entire database.
    """
    with database.SessionLocal() as session:
        data = crud.get_all(session)

    return data
