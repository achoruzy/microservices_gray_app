#   Copyright (C) 2021  Arkadiusz Choruzy
#
#   Arkadiusz Choruzy
#   achoruzy@gmail.com

from sqlalchemy.orm import Session

from . import schemas
from .db import models


def get_datarow(db: Session, datarow_id: int):
    return db.query(models.Data).filter(models.Data.id == datarow_id).first()
