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
    school_name: Optional[str],
    category: Optional[str],
):
    query = (
        db.query(models.Data)
        .filter_by(school_name=school_name, category=category)
        .all()
    )
