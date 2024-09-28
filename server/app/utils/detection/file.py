import aiohttp

from app.services import FileStorageService


async def get_uuid(link: str) -> str:
    return link.split("/")[-1].split(".mp4")[0]


async def download_video(uuid: str, link: str, file_service: FileStorageService):
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as resp:
            file_service.save(uuid, await resp.read())


async def remove_video(uuid: str, file_service: FileStorageService):
    file_service.delete(uuid, uuid)
