from fastapi.concurrency import run_in_threadpool

from app.db.connection import SessionManager
from app.db.repository import VideoFrameRepository, VideoItemRepository


async def run_detection_by_video(link: str, model):
    dataframe_task = run_in_threadpool(model.video2frames2embeddings, link, get_every_sec_frame=2.5)
    
    video_frame_repository = VideoFrameRepository()
    session_maker = SessionManager().get_session_maker()
    results = []
    async with session_maker() as session:
        dataframe = await dataframe_task
        for _, row in dataframe.iterrows():
            result = await video_frame_repository.get_nearest(session, row["embedding_data"])
            results.append(result)
    return results, dataframe


async def run_detection_by_text(link: str, model):
    tensor_task = run_in_threadpool(model.get_embedding_from_url, link)
    
    video_frame_repository = VideoItemRepository()
    session_maker = SessionManager().get_session_maker()
    results = []
    async with session_maker() as session:
        tensor = await tensor_task
        result = await video_frame_repository.get_nearest(session, tensor)
        results.append(result)
    return results, list(tensor)
