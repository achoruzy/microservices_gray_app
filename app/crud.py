#   Copyright (C) 2021  Arkadiusz Choruzy
#
#   Arkadiusz Choruzy
#   achoruzy@gmail.com

from typing import Optional

from sqlalchemy.orm import Session

import schemas
from db import models


def get_datarow(db: Session, datarow_id: int):
    return db.query(models.Data).filter(models.Data.id == datarow_id).first()


def get_all(db: Session):
    return db.query(models.Data).all()


def get_dataset_filtered(
    db: Session,
    school_name: Optional[str] = None,
    category: Optional[str] = None,
    gender: Optional[str] = None,
    more_than: Optional[int] = None,
    less_than: Optional[int] = None,
):

    query = db.query(models.Data)

    if school_name != None:
        query = query.filter_by(school_name=school_name)

    if category != None:
        query = query.filter_by(category=category)

    genders_available = [
        ["female", "girls", "girl", "women"],
        ["male", "boys", "boy", "men"],
        ["both", "all", "unisex"],
    ]

    if gender == None or gender.lower() in genders_available[2]:
        if more_than != None:
            query = query.filter(models.Data.total_enrollment > more_than)
        if less_than != None:
            query = query.filter(models.Data.total_enrollment < less_than)
    elif gender.lower() in genders_available[0]:
        if more_than != None:
            query = query.filter(models.Data.female > more_than)
        if less_than != None:
            query = query.filter(models.Data.female < less_than)
    elif gender.lower() in genders_available[1]:
        if more_than != None:
            query = query.filter(models.Data.male > more_than)
        if less_than != None:
            query = query.filter(models.Data.male < less_than)

    return query.all()
