import os

from celery import Celery


REDIS_URL = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")

celery_app = Celery(
    "worker",
    backend=REDIS_URL,
    broker=REDIS_URL,
    include=['app.tasks'],
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['application/json'],
    result_serializer='json',
    timezone='Asia/Krasnoyarsk',
)
