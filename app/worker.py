#   Copyright (C) 2021  Arkadiusz Choruzy
#
#   Arkadiusz Choruzy
#   achoruzy@gmail.com

import os
from celery import Celery
from celery.signals import worker_ready

# -- INTERNAL IMPORTS --
from db.build import build_db
import main


# -- CELERY CONFIGURATION --

os.environ.setdefault('C_FORCE_ROOT', 'true')

celery = Celery(__name__, include=['main'])

celery.conf.broker_url = os.environ.get(
    "CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://localhost:6379")
celery.conf.update(task_serializer='pickle',
                   event_serializer='pickle',
                   accept_content=['pickle', 'json'])


@worker_ready.connect
def on_worker_ready(**kwargs):
    """Celery worker function for database creation at docker container start."""

    try:
        build_db()
    except RuntimeError:
        print("Database haven't been build. An error occured.")
