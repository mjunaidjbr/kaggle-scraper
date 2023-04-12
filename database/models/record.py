from datetime import datetime
from sqlalchemy import (
    JSON,
    Text,
    String,
    Column,
    Integer,
    DateTime,
)

from database.base import Base


class Record(Base):
    __tablename__ = 'records'

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        unique=True,
        autoincrement=True
    )
    url = Column(
        String(1024),
        unique=True,
        nullable=False,
        index=True,
    )
    author = Column(
        String(255),
        default='Unknown',
        nullable=False,
        index=True,
    )
    title = Column(
        String(255),
        default='',
        nullable=False,
        index=True,
    )
    subtitle = Column(
        String(255),
        default='',
        nullable=False,
        index=True,
    )
    description = Column(
        Text,
        default='',
        nullable=False,
        index=True,
    )
    path = Column(
        String(512),
        default='',
        nullable=False,
        index=True,
    )
    download_url = Column(
        String(1024),
        default='',
        nullable=False,
        index=True,
    )
    tags = Column(
        JSON,
        default=[],
        nullable=False,
        index=True,
    )
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True,
    )
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True,
    )

    class Config:
        orm_mode = True

    def __repr__(self):
        return f"<Record(id={self.id}>"
