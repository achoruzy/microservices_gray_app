#   Copyright (C) 2021  Arkadiusz Choruzy
#
#   Arkadiusz Choruzy
#   achoruzy@gmail.com

from fastapi import FastAPI


api = FastAPI()


@api.get("/")
def read_root():
    return {"Hello": "World"}
