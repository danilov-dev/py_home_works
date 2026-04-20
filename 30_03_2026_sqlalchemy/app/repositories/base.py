from typing import Generic, TypeVar, Optional, List, Type
from sqlalchemy import select, func
from sqlalchemy.orm import sessionmaker
from ..core import Base

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], session_factory: sessionmaker):
        self.model = model
        self.session_factory = session_factory

    def get_by_id(self, entity_id: int) -> Optional[ModelType]:
        with self.session_factory() as session:
            return session.get(self.model, entity_id)

    def get_all(self, limit: int = 100, offset: int = 0) -> List[ModelType]:
        with self.session_factory() as session:
            stmt = select(self.model).offset(offset).limit(limit)
            return list(session.scalars(stmt).all())

    def get_count(self) -> int:
        with self.session_factory() as session:
            return session.scalar(select(func.count()).select_from(self.model)) or 0

    def create(self, obj_in: dict) -> ModelType:
        with self.session_factory() as session:
            obj = self.model(**obj_in)
            session.add(obj)
            session.commit()
            session.refresh(obj)
            return obj

    def update(self, entity_id: int, **kwargs) -> Optional[ModelType]:
        with self.session_factory() as session:
            obj = session.get(self.model, entity_id)
            if not obj: return None
            for field, value in kwargs.items():
                setattr(obj, field, value)
            session.commit()
            session.refresh(obj)
            return obj

    def delete(self, entity_id: int) -> bool:
        with self.session_factory() as session:
            obj = session.get(self.model, entity_id)
            if not obj: return False
            session.delete(obj)
            session.commit()
            return True