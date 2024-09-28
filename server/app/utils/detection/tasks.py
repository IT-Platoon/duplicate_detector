from time import perf_counter

from fastapi.concurrency import run_in_threadpool

from app.db.connection import SessionManager
from app.db.repository import VideoFrameRepository


async def run_detection_by_video(link: str, model):
    start = perf_counter()
    dataframe_task = run_in_threadpool(model.video2frames2embeddings, link, get_every_sec_frame=2.5)
    
    video_frame_repository = VideoFrameRepository()
    session_maker = SessionManager().get_session_maker()
    results = []
    async with session_maker() as session:
        dataframe = await dataframe_task
        for _, row in dataframe.iterrows():
            result = await video_frame_repository.get_nearest(session, row["embedding_data"])
            results.append(result)
    print(perf_counter() - start)
    print(results)
