#   Copyright (C) 2021  Arkadiusz Choruzy
#
#   Arkadiusz Choruzy
#   achoruzy@gmail.com

from sqlalchemy import Column, Text, Integer

# -- INTERNAL IMPORTS --
from app.db.database import Base, TABLE


class Data(Base):
    """ SQLalchemy ORM model for creation of a database.
    """
    __tablename__ = TABLE

    # DB columns - has to match with .database.COLUMNS
    id = Column(Integer, primary_key=True)
    school_name = Column(Text, nullable=False, unique=False)
    category = Column(Text, nullable=False, unique=False)
    total_enrollment = Column(Integer, nullable=False)
    female = Column(Integer, nullable=False)
    male = Column(Integer, nullable=False)
