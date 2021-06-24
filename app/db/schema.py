#   Copyright (C) 2021  Arkadiusz Choruzy
#
#   Arkadiusz Choruzy
#   achoruzy@gmail.com

from sqlalchemy import MetaData, Table, Column, Text, Integer, Float
from sqlalchemy import ForeignKey


metadata = MetaData()

school = Table(
    "school",
    metadata,
    Column("school_id", Integer, primary_key=True),
    Column("school_name", Text, nullable=False),
)

category = Table(
    "category",
    metadata,
    Column("category_id", Integer, primary_key=True),
    Column("category", Text, nullable=False),
)

school_data = Table(
    "school_data",
    metadata,
    Column("data_id", Integer, primary_key=True),
    Column("total_enrollment", Integer, nullable=False),
    Column("female", Integer, nullable=False),
    Column("male", Integer, nullable=False),
    Column("school_id", ForeignKey(school.c.school_id)),
    Column("category_id", ForeignKey(category.c.category_id)),
)
