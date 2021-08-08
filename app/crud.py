#   Copyright (C) 2021  Arkadiusz Choruzy
#
#   Arkadiusz Choruzy
#   achoruzy@gmail.com

from typing import Optional

from sqlalchemy.orm import Session

# -- INTERNAL IMPORTS --
from app.db import models


def get_datarow(db: Session, datarow_id: int) -> Session.query:
    """
    CRUD's READ function for retrieving only one datarow from a database.

    Args:
        db: sqlalchemy.orm.Session - session connection to the database
        datarow_id: int - datarow number to be retrieved

    Returns:
        json serialised data of desired row
    """
    query = db.query(models.Data).filter(models.Data.id == datarow_id).first()

    return query


def get_all(db: Session):
    """
    CRUD's READ function for retrieving all datarows from a database.

    Args:
        db: sqlalchemy.orm.Session - session connection to the database

    Returns:
        json serialised data
    """
    query = db.query(models.Data).all()

    return query


def get_dataset_filtered(
    db: Session,
    school_name: Optional[str] = None,
    category: Optional[str] = None,
    gender: Optional[str] = None,
    more_than: Optional[int] = None,
    less_than: Optional[int] = None,
):
    """
    CRUD's READ function for retrieving filtered data from a database.

    Args:
        db: sqlalchemy.orm.Session - session connection to the database
        school_name: Optional[str] - data filter
        category: Optional[str] - data filter
        gender: Optional[str] - data filter
        more_than: Optional[int] - data filter
        less_than: Optional[int] - data filter

    Returns:
        sqlalchemy.orm.Session.query - all of the filtered data
    """

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
