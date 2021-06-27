#   Copyright (C) 2021  Arkadiusz Choruzy
#
#   Arkadiusz Choruzy
#   achoruzy@gmail.com

from sqlalchemy import MetaData, Table, Column, Text, Integer, Float
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


metadata = MetaData()

school = Table(
    "school",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("school_name", Text, nullable=False, unique=True),
)

category = Table(
    "category",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("category", Text, nullable=False, unique=True),
)

school_data = Table(
    "school_data",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("total_enrollment", Integer, nullable=False),
    Column("female", Integer, nullable=False),
    Column("male", Integer, nullable=False),
    Column("school_id", ForeignKey(school.c.id)),
    Column("category_id", ForeignKey(category.c.id)),
)
