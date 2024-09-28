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
from app.tasks import run_detection
from app.utils.detection import get_uuid


api_router = APIRouter(
    tags=["Detection"],
)


@api_router.post(
    "check-video-duplicate",
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
    
    uuid = get_uuid(video.link)

    result = run_detection.delay(uuid) 
    return result
