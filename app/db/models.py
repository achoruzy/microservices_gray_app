#   Copyright (C) 2021  Arkadiusz Choruzy
#
#   Arkadiusz Choruzy
#   achoruzy@gmail.com

from sqlalchemy import Table, Column, Text, Integer

from . import database
from .database import Base, TABLE


class Data(Base):
    __tablename__ = TABLE

    id = Column(Integer, primary_key=True)
    school_name = Column(Text, nullable=False, unique=False)
    category = Column(Text, nullable=False, unique=False)
    total_enrollment = Column(Integer, nullable=False)
    female = Column(Integer, nullable=False)
    male = Column(Integer, nullable=False)
