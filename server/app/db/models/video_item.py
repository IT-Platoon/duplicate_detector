from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TEXT, TIMESTAMP
from sqlalchemy.orm import relationship

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

    video_frames = relationship(
        "VideoFrame",
        back_populates="video_item",
        lazy="joined",
    )
