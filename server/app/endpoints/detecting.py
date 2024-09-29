import asyncio
from datetime import datetime

from fastapi import (
    APIRouter,
    UploadFile,
    Depends,
    Body,
    HTTPException,
    Request,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession
import pandas as pd

from app.db.connection import get_session
from app.db.repository import VideoFrameRepository, VideoItemRepository
from app.services import ControlCenter
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
):
    if not video.link:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неверный запрос",
        )

    detection_tasks = {
        run_detection_by_video: request.app.state.video_detection_service,
    }
    result = []
    for detection_task, model in detection_tasks.items():
        result, _ = await detection_task(video.link, model)
        
    result = ControlCenter.is_dublicate(
        result,
        [],
        mul_video=1,
        mul_text=0.2,
        threshold=2,
    )
    return VideoLinkResponse(is_duplicate=result[0], duplicate_for=result[1])


@api_router.post(
    "/check-video-duplicate-file",
    status_code=status.HTTP_200_OK,
)
async def detect_duplicates_file(
    request: Request,
    file: UploadFile,
    session: AsyncSession = Depends(get_session),
):
    df = pd.read_csv(file.file)
    df["created"] = pd.to_datetime(df["created"])
    df.sort_values(by=['created'], inplace=True)

    list_created = []
    list_uuid = []
    list_link = []
    list_is_duplicate = []
    list_duplicate_for = []

    video_frame_repository = VideoFrameRepository()
    video_item_repository = VideoItemRepository()

    for _, row in df.iterrows():
        uuid = row['uuid']
        created = row['created']
        link = row['link']

        list_id_video, dataframe = await run_detection_by_video(
            link,
            request.app.state.video_detection_service,
        )

        result = ControlCenter.is_dublicate(
            list_id_video,
            [],
            mul_video=0.8,
            mul_text=0.2,
            threshold=3
        )

        is_duplicate = result[0]
        duplicate_for = ''
        if is_duplicate:
            row["id"] = row.pop("uuid")
            await video_item_repository.create(session, obj_in=dict(row))
            for _, item in dataframe.iterrows():
                await video_frame_repository.create(
                    session,
                    obj_in={"video_item_id": row["id"], "embedding": item["embedding_data"]},
                )
            duplicate_for = result[1]

        list_created.append(created)
        list_uuid.append(uuid)
        list_link.append(link)
        list_duplicate_for.append(duplicate_for)
        list_is_duplicate.append(is_duplicate)

    submission = pd.DataFrame({
        'created': list_created,
        'uuid': list_uuid,
        'link': list_link,
        'is_duplicate': list_is_duplicate,
        'duplicate_for': list_duplicate_for,
    })
    submission.to_csv('submission.csv', index=False)
