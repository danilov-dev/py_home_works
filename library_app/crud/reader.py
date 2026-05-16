import logging
from typing import Optional

from sqlalchemy import select

from library_app.models import Reader, Book


class ReaderRepository:
    def __init__(self, session):
        self.session = session
        self.logger = logging.getLogger(__name__)

    def get_by_id(self, reader_id):
        return self.session.scalar(
            select(Reader)
            .where(Reader.id == reader_id))

    def get_all(self):
        return self.session.scalar(select(Reader)).all()

    def add_reader(self, reader: Reader):
        self.session.add(reader)
        return reader

    def update_reader(self, reader_id: int, **kwargs) -> Optional[Reader]:
        reader = self.get_by_id(reader_id)
        if not reader:
            self.logger.warning("Reader not found")
            return None

        for key, value in kwargs.items():
            setattr(reader, key, value)
        return reader

    def delete_reader(self, reader_id: int) -> bool:
        reader = self.get_by_id(reader_id)
        if not reader:
            self.logger.warning("Reader not found")
            return False
        self.session.delete(reader)
        return True
