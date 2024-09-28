from pgvector.sqlalchemy import Vector
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TEXT, TIMESTAMP

from .base import BaseTable


class VideoItem(BaseTable):
    __tablename__ = "video_item"

    link = Column(
        "link",
        TEXT,
        nullable=False,
    )
    created = Column(
        "created",
        TIMESTAMP(timezone=True),
        nullable=False,
    )
    embedding = Column(
        "embedding",
        Vector(516),
        nullable=True,
    )
