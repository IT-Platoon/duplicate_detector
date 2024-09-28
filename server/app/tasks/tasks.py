import asyncio

from app.config import celery_app
from app.services import ModelVideo2Frames
from app.utils.celery import (
    run_detection as run_detection_async,
)


model = ModelVideo2Frames()


@celery_app.task
def run_detection(uuid: str):
    asyncio.run(run_detection_async(uuid, model))
