import logging
from typing import Any
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.query import Query
from models import Record

from .base import Base

DEFUALT_DB_URL = 'sqlite:///db.sqlite3'

logger = logging.getLogger(__name__)


class Database:
    """
    Database class

    :param db_url: database url
    :type db_url: str
    :param create_tables: create tables if not exists
    :type create_tables: bool

    :example:
        >>> from database import Database
        >>> db = Database()
        >>> db.get(Record, id=1)
        <Record(id=1, name='test')>
    """

    def __init__(self, db_url=DEFUALT_DB_URL, create_tables=True):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

        if create_tables:
            Base.metadata.create_all(self.engine)

    def get(self, cls, **kwargs) -> Any | None:
        """
        Get record from database

        :param cls: model class
        :type cls: sqlalchemy.ext.declarative.api.DeclarativeMeta
        :param kwargs: filter
        :type kwargs: dict

        :return: record
        :rtype: cls
        """
        try:
            session = self.Session()
            record = session.query(cls).get(**kwargs)
            session.close()
            return record
        except Exception as e:
            logger.error(f'Error while getting record: {e}')
            raise e

    def filter(self, cls, **kwargs) -> Query:
        """
        Get record from database

        :param cls: model class
        :type cls: sqlalchemy.ext.declarative.api.DeclarativeMeta
        :param kwargs: filter
        :type kwargs: dict

        :return: Filtered query
        :rtype: Query
        """
        try:
            session = self.Session()
            record = session.query(cls).filter_by(**kwargs)
            session.close()
            return record
        except Exception as e:
            logger.error(f'Error while getting record: {e}')
            raise e

    def add(self, record: Any) -> None:
        """
        Add record to database

        :param record: record
        :type record: Any
        """
        try:
            session = self.Session()
            session.add(record)
            session.commit()
            session.close()
        except Exception as e:
            logger.error(f'Error while adding record: {e}')
            raise e
