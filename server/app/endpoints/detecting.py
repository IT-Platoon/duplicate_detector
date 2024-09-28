import asyncio

from fastapi import (
    APIRouter,
    Depends,
    Body,
    HTTPException,
    Request,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connection import get_session
from app.schemas.detection import VideoLinkRequest, VideoLinkResponse
from app.utils.detection import run_detection_by_video, run_detection_by_text


api_router = APIRouter(
    tags=["Detection"],
)


@api_router.post(
    "/check-video-duplicate",
    response_model=VideoLinkResponse,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Неверный запрос",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Ошибка сервера",
        },
    },
)
async def detect_duplicates(
    request: Request,
    video: VideoLinkRequest = Body(...),
    session: AsyncSession = Depends(get_session),
):
    if not video.link:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неверный запрос",
        )

    detection_tasks = {
        run_detection_by_video: request.app.state.video_detection_service,
        run_detection_by_text: request.app.state.text_detection_service,
    }
    tasks = []
    for detection_task, model in detection_tasks.items():
        task = detection_task(video.link, model)
        tasks.append(task)

    for completed_task in asyncio.as_completed(tasks):
        result = await completed_task
        print(result)
    # return result
