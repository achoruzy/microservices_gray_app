#   Copyright (C) 2021  Arkadiusz Choruzy
#
#   Arkadiusz Choruzy
#   achoruzy@gmail.com

from typing import Optional

from pydantic import BaseModel


class DataRowBase(BaseModel):
    """ Base pydantic data model for school data as json. """
    school_name: str
    category: str
    total_enrollment: int
    female: int
    male: int


class DataRowCreate(DataRowBase):
    """ Pydantic data model for inserting new data to school data as json. """
    pass


class DataRow(DataRowBase):
    """ Pydantic data model for single row of school data as json. """
    id: int

    class Config:
        orm_mode = True
