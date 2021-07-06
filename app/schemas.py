#   Copyright (C) 2021  Arkadiusz Choruzy
#
#   Arkadiusz Choruzy
#   achoruzy@gmail.com

from typing import Optional

from pydantic import BaseModel


class DataRowBase(BaseModel):
    school_name: str
    category: str
    total_enrollment: int
    female: int
    male: int


class DataRowCreate(DataRowBase):
    pass


class DataRow(DataRowBase):
    id: int

    class Config:
        orm_mode = True
