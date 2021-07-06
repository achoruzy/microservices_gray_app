#   Copyright (C) 2021  Arkadiusz Choruzy
#
#   Arkadiusz Choruzy
#   achoruzy@gmail.com

from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

from . import schemas
from .db import models, database


class Item(BaseModel):
    school_name: str


api = FastAPI()


@api.get("/")
def read_root():
    return {"Hello": "Kaszebe"}


@api.get("/filter")
async def filter_data(
    school_name: Optional[str] = None,
    category: Optional[str] = None,
    pupils_more_than: Optional[int] = None,
    pupils_less_than: Optional[int] = None,
    female: Optional[bool] = True,
    male: Optional[bool] = True,
):
    return {"school name": [school_name, category, pupils_more_than, female, male]}


@api.get("/datarow")
async def datarow():
    pass
