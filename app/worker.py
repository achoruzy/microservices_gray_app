#   Copyright (C) 2021  Arkadiusz Choruzy
#
#   Arkadiusz Choruzy
#   achoruzy@gmail.com

import os
import time
from celery import Celery
from celery.signals import worker_ready
from db.build import build_db


celery = Celery(__name__)
celery.conf.broker_url = os.environ.get(
    "CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://localhost:6379"
)


@worker_ready.connect
def on_worker_ready(**kwargs):
    """Celery worker function for database creation at docker container start."""

    try:
        build_db()
    except RuntimeError:
        print("Database haven't been build. An error occured.")
