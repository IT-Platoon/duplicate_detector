from app.db.connection import SessionManager
from app.db.repository import VideoItemRepository
from app.services import ModelVideo2Frames


async def run_detection(uuid: str, model: ModelVideo2Frames):
    video_item_repository = VideoItemRepository()
    session_maker = SessionManager().get_session_maker()
    async with session_maker() as session:
        pass
